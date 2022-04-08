import face_recognition

class Embedder:
    def __init__(self):
        pass
    
    @staticmethod
    def extractEmbeddings(image, box):
        return face_recognition.face_encodings(image, [box])[0]
