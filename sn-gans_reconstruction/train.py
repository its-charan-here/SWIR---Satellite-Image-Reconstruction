import os
import glob

import tensorflow as tf
import neuralgym as ng

from reconstruction_model import GAN_Reconstruction


def multigpu_graph_def(model, FLAGS, data, gpu_id=0, loss_type='g'):
    with tf.device('/cpu:0'):
        images = data.data_pipeline(FLAGS.batch_size)
    if gpu_id == 0 and loss_type == 'g':
        _, _, losses = model.build_graph_with_losses(
            FLAGS, images, FLAGS, summary=True, reuse=True)
    else:
        _, _, losses = model.build_graph_with_losses(
            FLAGS, images, FLAGS, reuse=True)
    if loss_type == 'g':
        return losses['g_loss']
    elif loss_type == 'd':
        return losses['d_loss']
    else:
        raise ValueError('loss type is not supported.')


if __name__ == "__main__":
    # training data
    FLAGS = ng.Config('sat_recontruction.yml') # ng is used for reading the Config files, i.e sat_reconstruction.yml
    print("Flags is:",FLAGS)
    img_shapes = FLAGS.img_shapes # set image shapes values (256,256)
    with open(FLAGS.data_flist[FLAGS.dataset][0]) as f:
        fnames = f.read().splitlines() # fnames consists of all training files

    data = ng.data.DataFromFNames(
        fnames, img_shapes, random_crop=FLAGS.random_crop,
        nthreads=FLAGS.num_cpus_per_job)
    images = data.data_pipeline(FLAGS.batch_size) # a pipeline is created having all the training images in queue.
    # main model
    model = GAN_Reconstruction() # object of put inpaint mondel 


    # print("\n\n\n\n",data,"\n\n\n\n")
    # print("\n\n\n\n",type(data),"\n\n\n\n")

    # print("\n\n\n\n",fnames,"\n\n\n\n")

    
    
    g_vars, d_vars, losses = model.build_graph_with_losses(FLAGS, images)
    # validation images
    if FLAGS.val:
        with open(FLAGS.data_flist[FLAGS.dataset][1]) as f:
            val_fnames = f.read().splitlines()

        # progress monitor by visualizing static images
        for i in range(FLAGS.static_view_size):
            # print("image:", i )
            static_fnames = val_fnames[i:i+1]
            static_images = ng.data.DataFromFNames(
                static_fnames, img_shapes, nthreads=1,
                random_crop=FLAGS.random_crop).data_pipeline(1)
            static_inpainted_images = model.build_static_infer_graph(
                FLAGS, static_images, name='static_view/%d' % i)


    
    # training settings
    lr = tf.get_variable('lr', shape=[], trainable=False,initializer=tf.constant_initializer(1e-4))
    d_optimizer = tf.train.AdamOptimizer(lr, beta1=0.5, beta2=0.999)
    g_optimizer = d_optimizer # initializing  optimizers (generotor and discrimiator is having the same optimizer)


    # train discriminator with secondary trainer, should initialize before primary trainer.
    # discriminator_training_callback = ng.callbacks.SecondaryTrainer(
    
    
    discriminator_training_callback = ng.callbacks.SecondaryMultiGPUTrainer( # initializing the discriminator 
        num_gpus=FLAGS.num_gpus_per_job,
        pstep=1,
        optimizer=d_optimizer, # calling the optimizer
        var_list=d_vars,
        max_iters=1,
        grads_summary=False,
        graph_def=multigpu_graph_def,
        graph_def_kwargs={
            'model': model, 'FLAGS': FLAGS, 'data': data, 'loss_type': 'd'},
    )
    # train generator with primary trainer
    # trainer = ng.train.Trainer(

    trainer = ng.train.MultiGPUTrainer( # inintializing the generator 
        num_gpus=FLAGS.num_gpus_per_job,
        optimizer=g_optimizer, 
        var_list=g_vars,# calling the discriminators optimizer
        max_iters=FLAGS.max_iters,
        graph_def=multigpu_graph_def,
        grads_summary=False,
        gradient_processor=None,
        graph_def_kwargs={
            'model': model, 'FLAGS': FLAGS, 'data': data, 'loss_type': 'g'},
        spe=FLAGS.train_spe,
        log_dir=FLAGS.log_dir,
    )
    # adding all callbacks to save the weights and restore from current epoch and display the summary of the model 


    trainer.add_callbacks([
        discriminator_training_callback,
        ng.callbacks.WeightsViewer(),
        ng.callbacks.ModelRestorer(trainer.context['saver'], dump_prefix=FLAGS.model_restore+'/snap', optimistic=True),
        ng.callbacks.ModelSaver(FLAGS.train_spe, trainer.context['saver'], FLAGS.log_dir+'/snap'),
        ng.callbacks.SummaryWriter((FLAGS.val_psteps//1), trainer.context['summary_writer'], tf.summary.merge_all()),
    ])




    # launch training
    trainer.train()
