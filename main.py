from flask import Flask, request, render_template
from kuaci import kuaci

# Initialize application
app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html', is_submit=False, data={})
    ktp = request.form['ktp']
    ctx = {'is_valid': False, 'ktp': ktp}
    if not kuaci.validator(ktp):
        return render_template('index.html', is_submit=True, data=ctx)
    ctx['is_valid'] = True
    ctx['area_code'] = ktp[:6]
    location = kuaci.locator(ctx['area_code'])
    ctx['province'] = location[1]
    ctx['district'] = location[2]
    ctx['subdistrict'] = location[3]
    ctx['gender'] = kuaci.gender_checker(ktp[6:7])
    try:
        dob = kuaci.dob_checker(ktp[6:12])
        ctx['dob'] = dob.strftime("%m/%d/%Y")
    except:
        ctx['dob'] = '-'
    return render_template('index.html', is_submit=True, data=ctx)
