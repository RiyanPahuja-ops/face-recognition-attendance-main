import fr
import database

database.mark_absent()
images = fr.student_images()
encodings = fr.find_encoding(images)
fr.recognize_face(encodings)

