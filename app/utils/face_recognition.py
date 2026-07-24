import face_recognition
import numpy as np
from PIL import Image
import io
import json

def get_face_vector(image_bytes: bytes) -> list:
    """
    Ekstrak 128D face encoding dari gambar bytes.
    Mengembalikan list float jika wajah ditemukan, atau None jika tidak ditemukan.
    """
    # Buka gambar menggunakan Pillow dan convert ke RGB
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(image)
    
    # Cari lokasi wajah
    face_locations = face_recognition.face_locations(image_np)
    if not face_locations:
        return None
        
    # Ekstrak encoding dari wajah pertama yang ditemukan
    face_encodings = face_recognition.face_encodings(image_np, face_locations)
    if not face_encodings:
        return None
        
    return face_encodings[0].tolist()

def compare_faces(known_vector_json: str, unknown_vector: list, threshold: float = 0.6) -> bool:
    """
    Bandingkan vektor terdaftar (di database dalam bentuk JSON) dengan vektor baru.
    """
    known_vector = np.array(json.loads(known_vector_json))
    unknown_vector_np = np.array(unknown_vector)
    
    # Hitung Euclidean distance
    distance = face_recognition.face_distance([known_vector], unknown_vector_np)[0]
    
    return distance <= threshold
