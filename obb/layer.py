from PIL import Image


class Layer:
    def __init__(self, frames, visibility=1):
        self.frames = frames
        self.visibility = visibility
        self.is_active = True

    def get_content(self, current_frame=0):
        return self.frames[current_frame].image

    def change_visibility(self, new_visibility):
        pass

    def add_frame(self, frame):
        self.frames.append(frame)

    def del_frame(self):
        del_frame = self.frames.pop(-1)
        del del_frame
