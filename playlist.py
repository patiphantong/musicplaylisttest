class song:
    def __init__(self, title):
        self.title = title
        self.next = None
        self.prev = None


class Stack:
    def __init__(self):
        self.items = []

    def is_Empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_Empty():
            return None
        return self.items.pop()

    def clear(self):
        self.items = []


class Playlist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0
        self.history = Stack()

    def add(self, title):
        new_song = song(title)
        if self.head is None:
            self.head = new_song
            self.tail = new_song
            new_song.prev = new_song
            new_song.next = new_song
            self.current = new_song
        else:
            new_song.prev = self.tail
            new_song.next = self.head
            self.tail.next = new_song
            self.head.prev = new_song
            self.tail = new_song
        self.size += 1

    def next_song(self):
        if self.head is None:
            return None
        if self.current is None:
            self.current = self.head
        else:
            self.history.push(self.current)
            self.current = self.current.next
        return self.current.title

    def previous_song(self):
        if self.head is None:
            return None
        if self.current is None:
            self.current = self.tail
        else:
            self.history.push(self.current)
            self.current = self.current.prev
        return self.current.title

    def play_song(self):
        if self.head is None:
            return None
        if self.current is None:
            self.current = self.head
        return self.current.title

    def insert_after_current(self, title):
        if self.head is None:
            new_song = song(title)
            self.head = new_song
            self.tail = new_song
            self.current = new_song
            new_song.next = new_song
            new_song.prev = new_song
            self.size += 1
            return
        if self.current is None:
            self.current = self.head
        new_song = song(title)
        new_song.prev = self.current
        new_song.next = self.current.next
        self.current.next.prev = new_song
        self.current.next = new_song
        if self.current == self.tail:
            self.tail = new_song
        # ไม่เปลี่ยน self.current เพราะ Insert มีหน้าที่เพิ่มเพลงเท่านั้น
        self.size += 1

    def remove_current_song(self):
        if self.head is None:
            return False
        if self.current is None:
            self.current = self.head
        if self.size == 1:
            self.head = None
            self.tail = None
            self.current = None
        else:
            next_song_node = self.current.next
            self.current.prev.next = self.current.next
            self.current.next.prev = self.current.prev
            if self.current == self.head:
                self.head = next_song_node
            if self.current == self.tail:
                self.tail = self.current.prev
            self.current = next_song_node
        self.size -= 1
        self.history.clear()
        return True

    def remove_song(self, title):
        if self.head is None:
            return False
        current = self.head
        for _ in range(self.size):
            if current.title == title:
                if self.size == 1:
                    self.head = None
                    self.tail = None
                    self.current = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    if current == self.head:
                        self.head = current.next
                    if current == self.tail:
                        self.tail = current.prev
                    if current == self.current:
                        self.current = current.next
                self.size -= 1
                self.history.clear()
                return True
            current = current.next
        return False

    def show_playlist(self):
        songs = []
        if self.head is None:
            return songs
        current = self.head
        for _ in range(self.size):
            songs.append(current.title)
            current = current.next
        return songs

    def show_reverse(self):
        songs = []
        if self.tail is None:
            return songs
        current = self.tail
        for _ in range(self.size):
            songs.append(current.title)
            current = current.prev
        return songs

    def history_back(self):
        if self.history.is_Empty():
            return None
        self.current = self.history.pop()
        return self.current.title

    def get_state(self):
        playlist = self.show_playlist()
        reverse = self.show_reverse()
        current_title = self.current.title if self.current else None
        return {
            "songs": playlist,
            "reverse_songs": reverse,
            "current": current_title,
            "size": self.size,
            "history_count": len(self.history.items),
        }
