from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sql

app = Flask(__name__)
app.secret_key="test@1234"

@app.route("/", methods=["GET","POST"])
def login():
    if "username" in session:
        return redirect(url_for("home"))
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        req_sent=sql.maintain(email,password)
        if email=="admin@10" and password=="admin10":
            return redirect(url_for("admin"))
        if req_sent[0]=="Verified":
            session["username"]=req_sent[1]
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("login"))  

@app.route("/signin", methods=["GET","POST"]) 
def signin():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        email=request.form.get("email")
        sql.user_insert(username,password,email)
        session["username"]=username
        return redirect(url_for("home"))
    


@app.route("/home")
def home():
    if "username" in session:
        username=session["username"]
        return render_template("home.html")
    else:
        redirect(url_for("login"))

@app.route("/jee", methods=["GET","POST"])
def jee():
    if "username" in session:
        username=session["username"]
        if request.method=="POST":
            pchapters=request.form.getlist("p")
            cchapters=request.form.getlist("c")
            mchapters=request.form.getlist("m")
            lvl=request.form.get("difficulty")

            output=[]
            base = {"PHYSICS":tuple(pchapters),"CHEMISTRY":tuple(cchapters),"MATHS":tuple(mchapters)}
            for i in base:
                if base[i]!=[]:
                    try:
                        output+=sql.result(f'{i}',base[i],lvl)
                    except:
                        pass

            return render_template("jee.html", ques=output,name=username)
        return render_template("jee.html",name=username)
    else:
        return redirect(url_for("login"))

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method=="POST":
        sub=request.form.get("subject")
        chap=request.form.get("chapter")
        lvl=request.form.get("level")
        ques=request.form.get("question")
        options=request.form.getlist("opt")
        answer=request.form.get("answer")
        sql.insert(sub,chap,lvl,ques,options,answer)
    return render_template("admin.html")

@app.route("/test" , methods=["GET","POST"])
def test():
    generated_paper=sql.createpaper()
    #print(generated_paper)
    if request.method=="POST":
        return generated_paper
    else:
        return render_template("test.html")
    

@app.route("/evaluate" , methods=["GET","POST"])
def evaluate():
    if request.method=="POST":
        got_data=request.get_json()
        print("gotdata: ", got_data)
        PHYSICS={}
        CHEMISTRY={}
        MATHS={}
        for i in got_data.keys():
            if i[1]=="P":
                t=sql.anything(f'select answer from physics where id="{i}"')
                PHYSICS[i]=t
            elif i[1]=="C":
                t=sql.anything(f'select answer from chemistry where id="{i}"')
                CHEMISTRY[i]=t
            elif i[1]=="M":
                t=sql.anything(f'select answer from maths where id="{i}"')
                MATHS[i]=t

        answer={"PHYSICS":PHYSICS,"CHEMISTRY":CHEMISTRY,"MATHS":MATHS}
        print("sentdata: ",answer)
        return answer

@app.route("/<name>")
def user(name):
    return render_template("user.html",username= session['username'])

@app.route("/prototype" , methods=["GET","POST"])
def prototye():
    if request.method=="POST":
        foo=request.form.getlist("try1")
        print(foo)
    return render_template("try.html")
    





if __name__ == "__main__":
    app.run(debug=True)