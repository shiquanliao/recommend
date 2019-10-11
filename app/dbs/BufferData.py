class RedisBufferData(object):
    def __init__(self):
        self.hot_key_tag_buffer = None
        self.user_key_tag_buffer = None

    def have_buffer(self):
        return self.hot_key_tag_buffer is not None \
               and self.user_key_tag_buffer is not None

    def set_hot_key_tag_buffer(self, hot_key_tag_buffer):
        self.hot_key_tag_buffer = hot_key_tag_buffer

    def set_user_key_tag_buffer(self, user_key_tag_buffer):
        self.user_key_tag_buffer = user_key_tag_buffer

    def get_hot_key_tag_buffer(self):
        return self.hot_key_tag_buffer

    def get_user_key_tag_buffer(self):
        return self.user_key_tag_buffer
