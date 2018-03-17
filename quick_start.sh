#echo download VOC dataset
#LINKS="
#http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
#http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar
#http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar
#"
#ROOT=/home/lindell/workspace/dahlia/yolo2-pytorch/data
#for LINK in $LINKS
#do
#	aria2c --auto-file-renaming=false -d $ROOT $LINK
#	tar -kxvf $ROOT/$(basename $LINK) -C $ROOT
#done

#echo cache data
#python3 cache.py -m cache/datasets=cache.voc.cache cache/name=cache_voc cache/category=config/category/20
#
ROOT=/home/lindell/workspace/dahlia/yolo2-pytorch/model/darknet
#
echo test VOC models
MODELS="
yolo-voc
tiny-yolo-voc
"
#
for MODEL in $MODELS
do
#	aria2c --auto-file-renaming=false -d $ROOT http://pjreddie.com/media/files/$MODEL.weights
#	python3 convert_darknet_torch.py $ROOT/$MODEL.weights -c config.ini config/darknet/$MODEL.ini -d
#    echo evaluating
#	python3 eval.py -c config.ini config/darknet/$MODEL.ini
    echo detecting
	python3 detect.py -c config.ini config/darknet/$MODEL.ini -i image.jpg --pause
done

#echo convert pretrained Darknet model
#aria2c --auto-file-renaming=false -d $ROOT http://pjreddie.com/media/files/darknet19_448.conv.23
#python3 convert_darknet_torch.py $ROOT/darknet19_448.conv.23 -m model/name=model_voc model/dnn=model.yolo2.Darknet -d --copy $ROOT/darknet19_448.conv.23.pth

#echo reproduce the training results
#export CACHE_NAME=cache_voc MODEL_NAME=model_voc MODEL=model.yolo2.Darknet
#python3 train.py -b 16 -lr 1e-3 -e 160 -m cache/name=$CACHE_NAME model/name=$MODEL_NAME model/dnn=$MODEL train/optimizer='lambda params, lr: torch.optim.SGD(params, lr, momentum=0.9)' train/scheduler='lambda optimizer: torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[60, 90], gamma=0.1)' -f $ROOT/darknet19_448.conv.23.pth -d
#python3 eval.py -m cache/name=$CACHE_NAME model/name=$MODEL_NAME model/dnn=$MODEL
