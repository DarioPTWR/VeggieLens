from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Array of images
imageArr = [
    "Bean1.jpg", "Bean2.jpg", "Bean3.jpg", "Bean4.jpg", "Bean5.jpg", "Bean6.jpg", "Bean7.jpg", "Bean8.jpg", "Bean9.jpg", "Bean10.jpg", "Bean11.jpg", "Bean12.jpg", "Bean13.jpg", "Bean14.jpg", "Bean15.jpg",
    "BitterGourd1.jpg", "BitterGourd2.jpg", "BitterGourd3.jpg", "BitterGourd4.jpg", "BitterGourd5.jpg", "BitterGourd6.jpg", "BitterGourd7.jpg", "BitterGourd8.jpg", "BitterGourd9.jpg", "BitterGourd10.jpg", "BitterGourd11.jpg", "BitterGourd12.jpg", "BitterGourd13.jpg", "BitterGourd14.jpg", "BitterGourd15.jpg",
    "BottleGourd1.jpg", "BottleGourd2.jpg", "BottleGourd3.jpg", "BottleGourd4.jpg", "BottleGourd5.jpg", "BottleGourd6.jpg", "BottleGourd7.jpg", "BottleGourd8.jpg", "BottleGourd9.jpg", "BottleGourd10.jpg", "BottleGourd11.jpg", "BottleGourd12.jpg", "BottleGourd13.jpg", "BottleGourd14.jpg", "BottleGourd15.jpg",
    "Brinjal1.jpg", "Brinjal2.jpg", "Brinjal3.jpg", "Brinjal4.jpg", "Brinjal5.jpg", "Brinjal6.jpg", "Brinjal7.jpg", "Brinjal8.jpg", "Brinjal9.jpg", "Brinjal10.jpg", "Brinjal11.jpg", "Brinjal12.jpg", "Brinjal13.jpg", "Brinjal14.jpg", "Brinjal15.jpg",
    "Broccoli1.jpg", "Broccoli2.jpg", "Broccoli3.jpg", "Broccoli4.jpg", "Broccoli5.jpg", "Broccoli6.jpg", "Broccoli7.jpg", "Broccoli8.jpg", "Broccoli9.jpg", "Broccoli10.jpg", "Broccoli11.jpg", "Broccoli12.jpg", "Broccoli13.jpg", "Broccoli14.jpg", "Broccoli15.jpg",
    "Cabbage1.jpg", "Cabbage2.jpg", "Cabbage3.jpg", "Cabbage4.jpg", "Cabbage5.jpg", "Cabbage6.jpg", "Cabbage7.jpg", "Cabbage8.jpg", "Cabbage9.jpg", "Cabbage10.jpg", "Cabbage11.jpg", "Cabbage12.jpg", "Cabbage13.jpg", "Cabbage14.jpg", "Cabbage15.jpg",
    "Capsicum1.jpg", "Capsicum2.jpg", "Capsicum3.jpg", "Capsicum4.jpg", "Capsicum5.jpg", "Capsicum6.jpg", "Capsicum7.jpg", "Capsicum8.jpg", "Capsicum9.jpg", "Capsicum10.jpg", "Capsicum11.jpg", "Capsicum12.jpg", "Capsicum13.jpg", "Capsicum14.jpg", "Capsicum15.jpg",
    "Carrot1.jpg", "Carrot2.jpg", "Carrot3.jpg", "Carrot4.jpg", "Carrot5.jpg", "Carrot6.jpg", "Carrot7.jpg", "Carrot8.jpg", "Carrot9.jpg", "Carrot10.jpg", "Carrot11.jpg", "Carrot12.jpg", "Carrot13.jpg", "Carrot14.jpg", "Carrot15.jpg",
    "Cauliflower1.jpg", "Cauliflower2.jpg", "Cauliflower3.jpg", "Cauliflower4.jpg", "Cauliflower5.jpg", "Cauliflower6.jpg", "Cauliflower7.jpg", "Cauliflower8.jpg", "Cauliflower9.jpg", "Cauliflower10.jpg", "Cauliflower11.jpg", "Cauliflower12.jpg", "Cauliflower13.jpg", "Cauliflower14.jpg", "Cauliflower15.jpg",
    "Cucumber1.jpg", "Cucumber2.jpg", "Cucumber3.jpg", "Cucumber4.jpg", "Cucumber5.jpg", "Cucumber6.jpg", "Cucumber7.jpg", "Cucumber8.jpg", "Cucumber9.jpg", "Cucumber10.jpg", "Cucumber11.jpg", "Cucumber12.jpg", "Cucumber13.jpg", "Cucumber14.jpg", "Cucumber15.jpg",
    "Papaya1.jpg", "Papaya2.jpg", "Papaya3.jpg", "Papaya4.jpg", "Papaya5.jpg", "Papaya6.jpg", "Papaya7.jpg", "Papaya8.jpg", "Papaya9.jpg", "Papaya10.jpg", "Papaya11.jpg", "Papaya12.jpg", "Papaya13.jpg", "Papaya14.jpg", "Papaya15.jpg",
    "Potato1.jpg", "Potato2.jpg", "Potato3.jpg", "Potato4.jpg", "Potato5.jpg", "Potato6.jpg", "Potato7.jpg", "Potato8.jpg", "Potato9.jpg", "Potato10.jpg", "Potato11.jpg", "Potato12.jpg", "Potato13.jpg", "Potato14.jpg", "Potato15.jpg",
    "Pumpkin1.jpg", "Pumpkin2.jpg", "Pumpkin3.jpg", "Pumpkin4.jpg", "Pumpkin5.jpg", "Pumpkin6.jpg", "Pumpkin7.jpg", "Pumpkin8.jpg", "Pumpkin9.jpg", "Pumpkin10.jpg", "Pumpkin11.jpg", "Pumpkin12.jpg", "Pumpkin13.jpg", "Pumpkin14.jpg", "Pumpkin15.jpg",
    "Radish1.jpg", "Radish2.jpg", "Radish3.jpg", "Radish4.jpg", "Radish5.jpg", "Radish6.jpg", "Radish7.jpg", "Radish8.jpg", "Radish9.jpg", "Radish10.jpg", "Radish11.jpg", "Radish12.jpg", "Radish13.jpg", "Radish14.jpg", "Radish15.jpg",
    "Tomato1.jpg", "Tomato2.jpg", "Tomato3.jpg", "Tomato4.jpg", "Tomato5.jpg", "Tomato6.jpg", "Tomato7.jpg", "Tomato8.jpg", "Tomato9.jpg", "Tomato10.jpg", "Tomato11.jpg", "Tomato12.jpg", "Tomato13.jpg", "Tomato14.jpg", "Tomato15.jpg",
]

# Dataset columns
ai_description = {
    "vgg31": {
        "description": "VGG is a model with a uniform architecture with consecutive convolution layers using 3 x 3 filters.",
        "31 x 31 px": {
          "train": 99.84,
          "test": 96.43
        }
    },
    "alexnet128": {
        "description": "AlexNet is a model that has groundbreaking CNN with ReLU activations, max pooling and dropout.",
        "128 x 128 px": {
          "train": 99.26,
          "test": 95.27
        }
    },
}

dataset_description = {
    "31 x 31 px": {
        "description": "This dataset is a dataset with 31 x 31 pixel images belonging to 15 classes from Bean to Tomato.",
        "classLabels":  {
            0: "Bean",
            1: "Bitter Gourd",
            2: "Bottle Gourd",
            3: "Brinjal",
            4: "Broccoli",
            5: "Cabbage",
            6: "Capsicum",
            7: "Carrot",
            8: "Cauliflower",
            9: "Cucumber",
            10: "Papaya",
            11: "Potato",
            12: "Pumpkin",
            13: "Radish",
            14: "Tomato"
        }
    },
    "128 x 128 px": {
        "description": "This dataset is a dataset with 128 x 128 pixel images belonging to 15 classes from Bean to Tomato.",
        "classLabels":  {
            0: "Bean",
            1: "Bitter Gourd",
            2: "Bottle Gourd",
            3: "Brinjal",
            4: "Broccoli",
            5: "Cabbage",
            6: "Capsicum",
            7: "Carrot",
            8: "Cauliflower",
            9: "Cucumber",
            10: "Papaya",
            11: "Potato",
            12: "Pumpkin",
            13: "Radish",
            14: "Tomato"
        }
    },
}

# Instantiate SQLAlchemy to handle DB Process
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.cfg')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from .models import User  # Import here to ensure it's after db initialization
        db.create_all()

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app