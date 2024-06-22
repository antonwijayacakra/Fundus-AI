from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from markupsafe import Markup

# Initialize the Flask application
app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/eye_disease_prediction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load the pre-trained Keras models
models = {
    'xception': load_model('Model_AI/model-xception_fatih.h5'),
    'mobilenet': load_model('Model_AI/mobilenetV1_model_tensorflowNew.h5'),
    'vgg16': load_model('Model_AI/vgg16_model_Tensorflownew.h5')
}

# Define a function to load and preprocess the image
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Rescale image
    return img_array

condition_explanations = {
    'DR': Markup('''<h1>Diabetic Retinopathy</h1>
    <p>Diabetic retinopathy adalah komplikasi diabetes yang memengaruhi mata. Kondisi ini terjadi ketika tingginya kadar gula darah menyebabkan kerusakan pada pembuluh darah kecil di retina, yaitu jaringan sensitif cahaya yang terletak di bagian belakang mata. Diabetic retinopathy dapat menyebabkan pembengkakan, kebocoran, atau bahkan pertumbuhan pembuluh darah baru yang abnormal pada retina, yang pada akhirnya bisa menyebabkan kebutaan jika tidak diobati.</p>

    <h1>Tahapan Diabetic Retinopathy</h1>
    
        <p>◉Retinopati Non-Proliferatif (Non-Proliferative Diabetic Retinopathy - NPDR)</p>
        <p>◉Retinopati Proliferatif (Proliferative Diabetic Retinopathy - PDR)</p>


    <h1>Penanganan Diabetic Retinopathy</h1>
    <p>Penanganan diabetic retinopathy bertujuan untuk memperlambat atau menghentikan perkembangan penyakit dan mencegah kebutaan. Berikut adalah beberapa metode penanganannya:</p>
    
        <p>◉Pengendalian Gula Darah</p>
        <p>◉Terapi Laser (Fotokoagulasi)</p>
        <p>◉Suntikan Obat Anti-VEGF</p>
        <p>◉Vitrektomi</p>
        <p>◉Pengendalian Faktor Risiko</p>


    <h1>Pencegahan</h1>
    <p>Pencegahan diabetic retinopathy melibatkan kontrol diabetes yang baik, termasuk:</p>
   
        <p>◉Pemantauan rutin kadar gula darah</p>
        <p>◉Pemeriksaan mata secara berkala</p>
        <p>◉Diet sehat dan olahraga teratur</p>
        <p>◉Menghindari merokok</p>
    '''),
    'glaucoma': Markup(''' <h1>Glaukoma</h1>
    <p>Glaukoma adalah sekelompok penyakit mata yang merusak saraf optik mata, yang vital untuk penglihatan yang baik. Kerusakan ini sering disebabkan oleh tekanan yang sangat tinggi di mata (tekanan intraokular). Glaukoma adalah salah satu penyebab utama kebutaan bagi orang di atas 60 tahun. Ini bisa terjadi pada usia berapa pun tetapi lebih sering terjadi pada orang dewasa yang lebih tua.</p>

    <h1>Jenis-jenis Glaukoma</h1>
    
        <p>◉Glaukoma Sudut Terbuka (Open-Angle Glaucoma)</strong>: Ini adalah bentuk glaukoma yang paling umum.</p>
        <p>◉Glaukoma Sudut Tertutup (Angle-Closure Glaucoma)</strong>: Ini adalah kondisi yang kurang umum tetapi lebih parah.</p>
        <p>◉Glaukoma Tekanan Normal (Normal-Tension Glaucoma)</strong>: Dalam jenis ini, saraf optik rusak meskipun tekanan mata dalam kisaran normal.</p>
        <p>◉Glaukoma Kongenital</strong>: Jenis ini terjadi pada bayi yang lahir dengan cacat pada sudut drainase mata yang memperlambat atau mencegah drainase normal cairan mata.</p>
        <p>◉Glaukoma Sekunder</strong>: Jenis ini terjadi akibat kondisi atau penyakit lain.</p>


    <h1>Gejala Glaukoma</h1>
    <p>Gejala glaukoma bisa bervariasi tergantung pada jenisnya:</p>
   
        <p>◉Untuk Glaukoma Sudut Terbuka: Kehilangan penglihatan dimulai dari tepi penglihatan (peripheral vision).</p>
        <p>◉Untuk Glaukoma Sudut Tertutup: Gejala bisa tiba-tiba dan parah.</p>
    

    <h1>Penanganan Glaukoma</h1>
    <p>Penanganan glaukoma berfokus pada menurunkan tekanan intraokular untuk mencegah kerusakan lebih lanjut pada saraf optik. Beberapa metode penanganan meliputi:</p>
    
        <p>◉Obat Tetes Mata</p>
        <p>◉Obat Oral</p>
        <p>◉Terapi Laser</p>
        <p>◉Pembedahan</p>


    <h1>Pencegahan</h1>
    <p>Sementara glaukoma tidak dapat selalu dicegah, beberapa langkah dapat membantu mengurangi risiko:</p>
   
        <p>◉Pemeriksaan Mata Rutin</p>
        <p>◉Mengetahui Riwayat Keluarga</p>
        <p>◉Olahraga Teratur</p>
        <p>◉Mengambil Obat Mata Sesuai Rekomendasi</p>
    '''),
    'normal': Markup(''' <h1>Mata Normal</h1>
    <p>Mata normal adalah mata yang tidak mengalami gangguan penglihatan atau penyakit mata yang serius. Ini adalah kondisi mata yang optimal, di mana semua struktur mata berfungsi dengan baik.</p>

    <h1>Fungsi Mata Normal</h1>
    <p>Mata normal memiliki kemampuan untuk:</p>
   
        <p>◉Menerima cahaya dan gambar melalui kornea dan lensa.</p>
        <p>◉Fokus gambar pada retina untuk membentuk gambar yang jelas.</p>
        <p>◉Mengirimkan sinyal visual dari retina ke otak melalui saraf optik.</p>
        <p>◉Mengatur jumlah cahaya yang masuk ke mata melalui iris.</p>
        <p>◉Menyesuaikan bentuk lensa untuk melihat objek pada jarak yang berbeda (akomodasi).</p>
    

    <h1>Pencegahan</h1>
    <p>Untuk menjaga kesehatan mata dan mencegah gangguan penglihatan, penting untuk:</p>
   
        <p>◉Memeriksakan mata secara teratur ke dokter mata untuk pemeriksaan rutin.</p>
        <p>◉Memakai kacamata atau lensa kontak jika diperlukan.</p>
        <p>◉Menghindari paparan langsung terhadap sinar UV dengan menggunakan kacamata hitam saat berada di bawah sinar matahari.</p>
        <p>◉Mengonsumsi makanan sehat yang kaya nutrisi, terutama makanan yang mengandung vitamin A, lutein, dan zeaxanthin.</p>
        <p>◉Menjaga kelembapan mata dengan menggunakan tetes mata buatan jika mata terasa kering.</p>
        <p>◉Menghindari kebiasaan merokok.</p>
        <p>◉Menjaga berat badan yang sehat dan mengelola kondisi kesehatan seperti diabetes dan tekanan darah tinggi.</p>
    ''')
}

# Define the Predictions model
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)  # New column for model name
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files or 'model' not in request.form:
            return redirect(request.url)

        file = request.files['file']
        selected_model = request.form['model']
        print(f"Selected model: {selected_model}")  # Debug statement
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            img_array = preprocess_image(file_path)
            model = models[selected_model]
            prediction = model.predict(img_array)

            predicted_class = np.argmax(prediction, axis=1)[0]
            class_labels = ['retinopathy', 'glaucoma', 'normal']
            predicted_label = class_labels[predicted_class]

            explanation = condition_explanations[predicted_label]

            new_prediction = Prediction(filename=filename, prediction=predicted_label, model=selected_model)
            print(f"New prediction: {new_prediction}")  # Debug statement
            db.session.add(new_prediction)
            db.session.commit()

            return render_template('index.html', filename=filename, prediction=predicted_label, explanation=explanation)

    return render_template('index.html', filename=None, prediction=None, explanation=None)


# Route to display uploaded file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/delete/<int:result_id>', methods=['POST'])
def delete_result(result_id):
    result = Prediction.query.get_or_404(result_id)
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('hasil'))

@app.route('/hasil')
def hasil():
    results = Prediction.query.order_by(Prediction.upload_date.desc()).all()
    return render_template('hasil.html', results=results)

# Route to display team members
@app.route('/anggota')
def anggota():
    return render_template('anggota.html')

# Route to display homepage
@app.route('/beranda')
def beranda():
    return render_template('beranda.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)
