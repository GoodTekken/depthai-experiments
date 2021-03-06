import cv2
import numpy as np
import depthai as dai
from time import sleep

'''
Basic demo of gen2 pipeline builder functionality where output of jpeg encoded images are sent out SPI rather than the typical XLink out interface.

Make sure you have something to handle the SPI protocol on the other end! See the included ESP32 example. 
'''

def create_spi_demo_pipeline():
    print("Creating SPI pipeline: ")
    print("COLOR CAM -> ENCODER -> SPI OUT")
    pipeline = dai.Pipeline()

    cam_color         = pipeline.create(dai.node.ColorCamera)
    spiout_preview    = pipeline.create(dai.node.SPIOut)
    videnc            = pipeline.create(dai.node.VideoEncoder)

    # set up color camera and link to NN node
    cam_color.setPreviewSize(300, 300);
    cam_color.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P);
    cam_color.setInterleaved(False);
    cam_color.setCamId(0);
    cam_color.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR);

    # VideoEncoder
    videnc.setDefaultProfilePreset(1920, 1080, 30, dai.VideoEncoderProperties.Profile.MJPEG);

    # Link plugins CAM -> ENCODER -> SPI OUT
    cam_color.video.link(videnc.input);
    spiout_preview.setStreamName("spipreview");
    spiout_preview.setBusId(0);
    videnc.bitstream.link(spiout_preview.input);

    return pipeline


def test_pipeline():
    pipeline = create_spi_demo_pipeline()

    print("Creating DepthAI device")
    if 1:
        device = dai.Device(pipeline)
    else: # For debug mode, with the firmware already loaded
        found, device_info = dai.XLinkConnection.getFirstDevice(
                dai.XLinkDeviceState.X_LINK_UNBOOTED)
        if found:
            device = dai.Device(pipeline, device_info)
        else:
            raise RuntimeError("Device not found")
    print("Starting pipeline")
    device.startPipeline()

    print("Pipeline is running. See connected SPI device for output!")

    while True:
        sleep(1)

    print("Closing device")
    del device

test_pipeline()
