class RedisBufferData(object):
    def __init__(self):
        self._hot_key_tag_buffer = None
        self._user_key_tag_buffer = None

    def have_buffer(self):
        return self._hot_key_tag_buffer is not None \
               and self._user_key_tag_buffer is not None

    def set_hot_key_tag_buffer(self, hot_key_tag_buffer):
        self._hot_key_tag_buffer = hot_key_tag_buffer

    def set_user_key_tag_buffer(self, user_key_tag_buffer):
        self._user_key_tag_buffer = user_key_tag_buffer

    def get_hot_key_tag_buffer(self, key):
        return self._hot_key_tag_buffer.get(key, -1)

    def get_user_key_tag_buffer(self, key):
        return self._user_key_tag_buffer.get(key, -1)
