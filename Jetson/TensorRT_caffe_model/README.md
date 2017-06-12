Se requiere clonar el proyecto de inferencia de la jetson:
https://github.com/dusty-nv/jetson-inference#multi-class-object-detection-models

Para empezar el reconocimiento es necesario estar en la ubicación /home/ubuntu/jetson-inference/build/aarch64/bin 

y ejecutar el siguiente comando: 
./detectnet-camera /home/ubuntu/RoboBoat_2017_Main/Jetson/fotos/0ad5e993-4225-4e15-877d-c9761f12d0a4.png output_boya.jpg --prototxt=$NET/deploy.prototxt --model=$NET/snapshot_iter_112800.caffemodel --input_blob=data --output_cvg=coverage --output_bbox=bboxes


si se desea hacer algo más con los puntos del bounding box(bbox), es necesario editar el archivo /home/ubuntu/jetson-inference/detectnet-camera/detecnet-camera.cpp (después de la línea 184 que es donde se despliega en la terminal los valores del recuadro) y hacer otra vez el make.

