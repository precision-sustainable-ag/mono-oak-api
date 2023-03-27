import depthai as dai

class CameraDevice():
    status = "inactive"
    _shared_borg_state = {}
    
    def __new__(cls, *args, **kwargs):
        obj = super(CameraDevice, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_borg_state
        return obj

    def upload_pipeline(self):        
        # Create pipeline
        pipeline = dai.Pipeline()

        # full resolution RGB
        cam_rgb = pipeline.create(dai.node.ColorCamera)
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
        cam_rgb.initialControl.setSharpness(0)   
        cam_rgb.initialControl.setLumaDenoise(0)  
        cam_rgb.initialControl.setChromaDenoise(4)
        
        script = pipeline.createScript()
        cam_rgb.isp.link(script.inputs['isp'])

        # script node for controlling frame rate getting to manip node
        script.setScript("""
            while True:
                frame = node.io['isp'].get()
                num = frame.getSequenceNum()
                if (num%30) == 0:
                    node.io['frame'].send(frame)
        """)

        # modifying isp frame and then feeding it to encoder
        manip = pipeline.create(dai.node.ImageManip)
        manip.initialConfig.setCropRect(0.006, 0, 1, 1)
        manip.setNumFramesPool(2)
        manip.setMaxOutputFrameSize(18385920)
        manip.initialConfig.setFrameType(dai.ImgFrame.Type.NV12)
        script.outputs['frame'].link(manip.inputImage)

        video_encoder = pipeline.create(dai.node.VideoEncoder)
        video_encoder.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
        video_encoder.setQuality(98)
        manip.out.link(video_encoder.input)

        xout_rgb = pipeline.create(dai.node.XLinkOut)
        xout_rgb.setStreamName("rgb")
        video_encoder.bitstream.link(xout_rgb.input)

        # preview rgb
        cam_rgb.setPreviewSize(640, 480)
        xout_preview = pipeline.create(dai.node.XLinkOut)
        xout_preview.setStreamName("preview")
        cam_rgb.preview.link(xout_preview.input)

        # mono_right
        mono_right = pipeline.create(dai.node.MonoCamera)
        xout_right = pipeline.create(dai.node.XLinkOut)
        xout_right.setStreamName("right")
        mono_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        mono_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
        # mono_right.out.link(xout_right.input)

        script_right = pipeline.createScript()
        mono_right.out.link(script_right.inputs['inr'])
        script_right.setScript("""
            while True:
                frame = node.io['inr'].get()
                num = frame.getSequenceNum()
                if (num%30) == 0:
                    node.io['framer'].send(frame)
        """)
        script_right.outputs['framer'].link(xout_right.input)

        # mono_left
        mono_left = pipeline.create(dai.node.MonoCamera)
        xout_left = pipeline.create(dai.node.XLinkOut)
        xout_left.setStreamName("left")
        mono_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
        mono_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
        # mono_left.out.link(xout_left.input)

        script_left = pipeline.createScript()
        mono_left.out.link(script_left.inputs['inl'])
        script_left.setScript("""
            while True:
                frame = node.io['inl'].get()
                num = frame.getSequenceNum()
                if (num%30) == 0:
                    node.io['framel'].send(frame)
        """)
        script_left.outputs['framel'].link(xout_left.input)

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
        self.status = "active"
        # DEVICE = self.device

    def close_pipeline(self):
        self.device.close()
        self.status = "inactive"

