from application.models import Entry
import datetime as datetime
import pytest
from flask import json
import base64
import pytz

# Change timezone to locale timezone
sgt = pytz.timezone('Asia/Singapore')

# Test 1 : Unexpected Failure Testing
@pytest.mark.parametrize("predictionList", [
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg",  "vgg31", "31 x 31 px", 12],
    [1, "./application/static/images/saved/325409-Cucumber.jpg",  "alexnet128", "128 x 128 px", 9],
    [1, "./application/static/images/saved/004101-Carrot7.jpg",  "vgg31", "31 x 31 px", 7],
    [1, "./application/static/images/saved/869837-Tomato9.jpg",  "alexnet128", "128 x 128 px", 14],
])

# Writing the test function class in the argument
def test_EntryClass(predictionList, capsys):
    with capsys.disabled():
        now = datetime.datetime.now(sgt)
        new_entry = Entry(
            user=predictionList[0],
            filePath=predictionList[1],
            modelType=predictionList[2],
            imageSize=predictionList[3],
            prediction=predictionList[4],
            predicted_on=now
        )
        assert new_entry.user == predictionList[0]
        assert new_entry.filePath == predictionList[1]
        assert new_entry.filePath[-4:] == ".png" or new_entry.filePath[-4:] == ".jpg" or new_entry.filePath[-5:] == ".jpeg"
        assert new_entry.modelType == predictionList[2]
        assert new_entry.modelType == "vgg31" or new_entry.modelType == "alexnet128"
        assert new_entry.imageSize == predictionList[3]
        assert new_entry.imageSize == "31 x 31 px" or new_entry.imageSize == "128 x 128 px"
        assert new_entry.prediction == predictionList[4]
        if new_entry.imageSize == "31 x 31 px" or new_entry.imageSize == "128 x 128 px":
            assert new_entry.prediction >= 0 and new_entry.prediction < 15
        assert new_entry.predicted_on == now

# Test 2 : Expected Failure Testing
    # What happens if the image path is invalid
    # What happens if the model type is not equal to "vgg31" or "alexnet128"
    # What happens if the image size if not equal to "31 x 31 px" or "128 x 128 px"
    # What happens if the prediction falls outside the range of 0-14

@pytest.mark.xfail(reason="Arguments fail due to testing.")
@pytest.mark.parametrize("predictionList", [
    # Fail due to invalid file path (Experimented with gifs, spreadsheets, invalid image extensions)
    [1, "./application/static/images/saved/696242-Pumpkin15.gif", "vgg31", "31 x 31 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.jp", "alexnet128", "128 x 128 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.pngg", "vgg31", "31 x 31 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "alexnet128", "128 x 128 px", 12],

    # Fail due to modelType not equal to "vgg31" or "alexnet128"
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "123vgg31", "31 x 31 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "123alexnet128", "128 x 128 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "1234vgg31", "31 x 31 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "1234alexnet128", "128 x 128 px", 12],

    # Fail due to image size not being equal to "31 x 31 px" or "128 x 128 px"
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "32 x 32 px", 15],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "alexnet128", "131 x 31 px", 15],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "1283 x 1283 px", 15],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "alexnet128", "313 x 331 px", 15],

    # Fail due to empty file path
    [1, "", "vgg31", "31 x 31 px", 12],
    [1, "", "alexnet128", "128 x 128 px", 12],
    [1, "", "vgg31", "31 x 31 px", 12],
    [1, "", "alexnet128", "128 x 128 px", 12],

    # Fail due to zero or negative image sizes
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "0 x 0 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "alexnet128", "-1 x -1 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "-31 x -31 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "alexnet128", "-128 x -128 px", 12],

    # Fail due to prediction being outside the range of classes [0-14]
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "31 x 31 px", -1],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "alexnet128", "128 x 128 px", -2],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "31 x 31 px", -3],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "alexnet128", "128 x 128 px", -4],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "31 x 31 px", 15],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "alexnet128", "128 x 128 px", 16],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "31 x 31 px", 17],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "alexnet128", "128 x 128 px", 18],
])
def test_EntryValidation(predictionList, capsys):
    test_EntryClass(predictionList, capsys)
        
# Test 3 : Testing the Add API
@pytest.mark.parametrize("predictionList", [
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "31 x 31 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "31 x 31 px", 12],
    [1, "./application/static/images/saved/922842-Cabbage15.jpg", "alexnet128", "128 x 128 px", 5],
    [1, "./application/static/images/saved/922842-Cabbage15.jpg", "alexnet128", "128 x 128 px", 5]
])
def test_addAPI(client, predictionList, capsys):
    with capsys.disabled():
        # Prepare the data into a dictionary
        predictData = {
            "user": predictionList[0],
            "imgPath": predictionList[1],
            "modelType": predictionList[2],
            "imageSize": predictionList[3],
            "prediction": predictionList[4],
        }
    response = client.post('/api/add', data=json.dumps(predictData), content_type="application/json",)
    # Check the outcome of the action
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["id"]
       
# Test 4 : Testing the Get API
# Please note : Parameters will change here depending on database records! Check DB to ensure such parameters exist!
@pytest.mark.parametrize("predictionList", [
    [1, 1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "31 x 31 px", 12],
    [2, 1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "31 x 31 px", 12],
    [3, 1, "./application/static/images/saved/922842-Cabbage15.jpg", "alexnet128", "128 x 128 px", 5],
    [4, 1, "./application/static/images/saved/922842-Cabbage15.jpg", "alexnet128", "128 x 128 px", 5]
])
def test_getAPI(client, predictionList, capsys):
    with capsys.disabled():
        response = client.get(f'/api/get/{predictionList[0]}')
        ret = json.loads(response.get_data(as_text=True))
        # Check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"] == predictionList[0]
        assert response_body["user"] == predictionList[1]
        assert response_body["filePath"] == predictionList[2]
        assert response_body["modelType"] == predictionList[3]
        assert response_body["imageSize"] == predictionList[4]
        assert response_body["prediction"] == predictionList[5]

# Test 5 : Testing the Delete API
@pytest.mark.parametrize("predictionList", [
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "31 x 31 px", 12],
    [1, "./application/static/images/saved/696242-Pumpkin15.jpg", "vgg31", "31 x 31 px", 12],
    [1, "./application/static/images/saved/922842-Cabbage15.jpg", "alexnet128", "128 x 128 px", 5],
    [1, "./application/static/images/saved/922842-Cabbage15.jpg", "alexnet128", "128 x 128 px", 5]
])
def test_deleteAPI(client, predictionList, capsys):
    with capsys.disabled():
        # prepare the data into a dictionary
        predictData = {
            "user": predictionList[0],
            "imgPath": predictionList[1],
            "modelType": predictionList[2],
            "imageSize": predictionList[3],
            "prediction": predictionList[4],
        }
    response = client.post('/api/add', data=json.dumps(predictData), content_type="application/json",)
    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["id"]
    id = response_body["id"]
    response2 = client.get(f'/api/delete/{id}')
    ret = json.loads(response2.get_data(as_text=True))
    # Check the outcome of the action
    assert response2.status_code == 200
    assert response2.headers["Content-Type"] == "application/json"
    response2_body = json.loads(response2.get_data(as_text=True))
    assert response2_body["result"] == "Ok! Delete Successful!"

# Test 6 : Consistency Test (Test Predict API)
@pytest.mark.parametrize("bigPredictionList", [
    [[1, "./application/static/images/saved/095856-Cauliflower10.jpg", "vgg31", "31 x 31 px", 8], 
     [1, "./application/static/images/saved/095856-Cauliflower10.jpg", "vgg31", "31 x 31 px", 8], 
     [1, "./application/static/images/saved/095856-Cauliflower10.jpg", "vgg31", "31 x 31 px", 8],
     [1, "./application/static/images/saved/095856-Cauliflower10.jpg", "vgg31", "31 x 31 px", 8],
     [1, "./application/static/images/saved/095856-Cauliflower10.jpg", "vgg31", "31 x 31 px", 8]],

    [[1, "./application/static/images/saved/758455-Potato14.jpg", "alexnet128", "128 x 128 px", 11],
     [1, "./application/static/images/saved/758455-Potato14.jpg", "alexnet128", "128 x 128 px", 11],
     [1, "./application/static/images/saved/758455-Potato14.jpg", "alexnet128", "128 x 128 px", 11],
     [1, "./application/static/images/saved/758455-Potato14.jpg", "alexnet128", "128 x 128 px", 11],
     [1, "./application/static/images/saved/758455-Potato14.jpg", "alexnet128", "128 x 128 px", 11]],

])
def test_predictAPI(client, bigPredictionList, capsys):
    predictOutput = []
    for predictionList in bigPredictionList:
        with capsys.disabled():
            with open(predictionList[1], "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode('utf-8')
                encoded_string = "data:image/png;base64," + encoded_string
            predictData = {
                "user": predictionList[0],
                "imageBlob": encoded_string,
                "imageName": predictionList[1].split("/")[-1],
                "model": predictionList[2],
                "dataset": predictionList[3],
                "prediction": predictionList[4],
            }            
            response = client.post('/api/predict', data=json.dumps(predictData), content_type="application/json",)
            # Check the outcome of the action
            assert response.status_code == 200
            assert response.headers["Content-Type"] == "application/json"
            response_body = json.loads(response.get_data(as_text=True))
            assert response_body["id"]
            predictOutput.append(response_body["prediction"])

        assert len(set(predictOutput)) <= 1