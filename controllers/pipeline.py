import depthai as dai
import numpy as np
import json
import socket
import time
import cv2

class CameraDevice():
    def upload_pipeline(self):
        pipeline = dai.Pipeline()

        cam_rgb = pipeline.create(dai.node.ColorCamera)
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)

        manip = pipeline.create(dai.node.ImageManip)
        manip.initialConfig.setCropRect(0.006, 0, 1, 1)
        manip.setNumFramesPool(2)
        manip.setMaxOutputFrameSize(18385920)
        manip.initialConfig.setFrameType(dai.ImgFrame.Type.NV12)
        cam_rgb.isp.link(manip.inputImage)

        video_encoder = pipeline.create(dai.node.VideoEncoder)
        video_encoder.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
        manip.out.link(video_encoder.input)

        xout_rgb = pipeline.createXLinkOut()
        xout_rgb.setStreamName("rgb")
        video_encoder.bitstream.link(xout_rgb.input)

        xout_rgb_p = pipeline.createXLinkOut()
        xout_rgb_p.setStreamName("preview")
        cam_rgb.preview.link(xout_rgb_p.input)

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

