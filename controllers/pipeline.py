import depthai as dai
import numpy as np
import json
import socket
import time
import cv2

class CameraDevice():
    def upload_pipeline(self):
        # Create pipeline
        pipeline = dai.Pipeline()

        camRgb = pipeline.create(dai.node.ColorCamera)
        camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)

        xoutRgb = pipeline.create(dai.node.XLinkOut)
        xoutRgb.setStreamName("rgb")
        camRgb.video.link(xoutRgb.input)

        xin = pipeline.create(dai.node.XLinkIn)
        xin.setStreamName("control")
        xin.out.link(camRgb.inputControl)

        # Properties
        videoEnc = pipeline.create(dai.node.VideoEncoder)
        videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
        camRgb.still.link(videoEnc.input)

        # Linking
        # xoutStill = pipeline.create(dai.node.XLinkOut)
        # xoutStill.setStreamName("preview")
        # videoEnc.bitstream.link(xoutStill.input)

        # mono_right
        mono_right = pipeline.create(dai.node.MonoCamera)
        xout_right = pipeline.create(dai.node.XLinkOut)
        xout_right.setStreamName("right")
        mono_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        mono_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
        mono_right.out.link(xout_right.input)

        # mono_left
        mono_left = pipeline.create(dai.node.MonoCamera)
        xoutLeft = pipeline.create(dai.node.XLinkOut)
        xoutLeft.setStreamName("left")
        mono_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
        mono_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
        mono_left.out.link(xoutLeft.input)

        # depth
        self.depth = pipeline.create(dai.node.StereoDepth)
        self.depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        self.depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
        self.depth.setLeftRightCheck(True)
        self.depth.setExtendedDisparity(False)
        self.depth.setSubpixel(False)

        xout_depth = pipeline.create(dai.node.XLinkOut)
        xout_depth.setStreamName("disparity")
        mono_right.out.link(self.depth.right)
        mono_left.out.link(self.depth.left)
        self.depth.disparity.link(xout_depth.input)

        self.device = dai.Device(pipeline)

        # still
        # xout_still = pipeline.create(dai.node.XLinkOut)
        # xout_still.setStreamName("still")
        # video_encoder.bitstream.link(xout_still.input)

    def close_pipeline(self):
        self.device.close()

