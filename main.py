import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import simpledialog
from tkinter import filedialog

def filtro_bn(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def filtro_desenfoque(img):
    return cv2.GaussianBlur(img, (15, 15), 0)

def save_image(image, img_type):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        cv2.imwrite(file_path, image)
        print(f"{img_type} image saved at {file_path}")

def main():
    global original, bn, desenfoque

    # Iniciar la captura de vídeo desde la cámara
    cap = cv2.VideoCapture(0)

    # Crear la ventana de la interfaz gráfica
    root = tk.Tk()
    root.title("Aplicación de Filtros")

    # Crear un lienzo para mostrar las imágenes, con márgenes
    img_width = 420
    img_height = 480
    margin = 15
    canvas_width = img_width * 3 + margin * 4
    canvas_height = img_height + margin * 2
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Variables para las imágenes de Tkinter
    img_original = None
    img_bn = None
    img_desenfoque = None

    def update_frame():
        global original, bn, desenfoque
        
        # Capturar frame a frame
        ret, frame = cap.read()
        if not ret:
            root.after(10, update_frame)
            return

        # Aplicar filtros
        bn = filtro_bn(frame)
        desenfoque = filtro_desenfoque(frame)

        # Convertir las imágenes de OpenCV a formato compatible con Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bn_rgb = cv2.cvtColor(bn, cv2.COLOR_GRAY2RGB)
        desenfoque_rgb = cv2.cvtColor(desenfoque, cv2.COLOR_BGR2RGB)

        img_original = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
        img_bn = ImageTk.PhotoImage(image=Image.fromarray(bn_rgb))
        img_desenfoque = ImageTk.PhotoImage(image=Image.fromarray(desenfoque_rgb))

        # Limpiar el lienzo
        canvas.delete("all")
        
        # Mostrar las imágenes en el lienzo con márgenes
        canvas.create_image(margin, margin, anchor=tk.NW, image=img_original)
        canvas.create_image(img_width + margin * 2, margin, anchor=tk.NW, image=img_bn)
        canvas.create_image(img_width * 2 + margin * 3, margin, anchor=tk.NW, image=img_desenfoque)

        # Guardar las imágenes de Tkinter para que no se recojan como basura
        canvas.img_original = img_original
        canvas.img_bn = img_bn
        canvas.img_desenfoque = img_desenfoque

        # Guardar los frames actuales para uso posterior
        original = frame
        bn = bn
        desenfoque = desenfoque

        # Programar la siguiente actualización
        root.after(10, update_frame)

    def on_key(event):
        if event.keysym == 'Escape':
            # Preguntar al usuario qué imagen desea guardar
            choice = simpledialog.askstring("Guardar imagen", "¿Qué imagen desea guardar? (original, bn, desenfoque):")
            if choice == "original":
                save_image(original, "Original")
            elif choice == "bn":
                save_image(bn, "Blanco y negro")
            elif choice == "desenfoque":
                save_image(desenfoque, "Desenfoque")
            else:
                print("Opción no válida.")

    # Iniciar la actualización de frames
    update_frame()

    # Asociar la función de captura de tecla
    root.bind("<Key>", on_key)

    # Ejecutar la interfaz gráfica
    root.mainloop()

    # Liberar la captura y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
