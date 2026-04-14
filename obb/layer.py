class Layer:
    def __init__(self, frames):
        self.frames = frames
        self.is_active = True

    def get_content(self, current_frame=0):
        return self.frames[current_frame].image

    def set_content(self, current_frame, image):
        self.frames[current_frame].image = image

    def add_frame(self, frame):
        self.frames.append(frame)

    def del_frame(self):
        del_frame = self.frames.pop(-1)
        del del_frame
