from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import pickle
import pandas as pd
import numpy as np
import json

# Load the model, scaler, and label encoders
scaler = pickle.load(open('scaler.pkl', 'rb'))
model = pickle.load(open('knn_model.pkl', 'rb'))
label_encoders = {
    'Type of Food': pickle.load(open('label_encoder_Type of Food.pkl', 'rb')),
    'Storage Conditions': pickle.load(open('label_encoder_Storage Conditions.pkl', 'rb')),
    'Event Type': pickle.load(open('label_encoder_Event Type.pkl', 'rb'))
}

# Predefined options
type_of_food_options = ['Meat (Kg)', 'Baked Goods(Kg)', 'Dairy Products(litre)', 'Fruits(kg)', 'Vegetables(Kg)']
event_type_options = ['Corporate', 'Social Gathering', 'Wedding', 'Birthday']
storage_conditions_options = ['Room Temperature', 'Refrigerated']

def knn_model(request):
    return render(request, 'knn.html',
                  {'type_of_food_options': type_of_food_options,
                   'event_type_options': event_type_options,
                   'storage_conditions_options': storage_conditions_options})

def predict(request):
    try:
        type_of_food = request.POST['type_of_food']
        quantity = float(request.POST['quantity'])
        event_type = request.POST['event_type']
        storage_conditions = request.POST['storage_conditions']

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        # Encode the input data
        encoded_type_of_food = label_encoders['Type of Food'].transform([type_of_food])[0]
        encoded_event_type = label_encoders['Event Type'].transform([event_type])[0]
        encoded_storage_conditions = label_encoders['Storage Conditions'].transform([storage_conditions])[0]

        # Prepare input data
        input_data = pd.DataFrame({
            'Type of Food': [encoded_type_of_food],
            'Quantity of food': [quantity],
            'Event Type': [encoded_event_type],
            'Storage Conditions': [encoded_storage_conditions]
        })

        # Scale input
        scaled_input = scaler.transform(input_data)

        # Predict
        prediction = model.predict(scaled_input)
        predicted_number_fed = round(prediction[0], 2)
        if predicted_number_fed < 0:
            predicted_number_fed = 0

        return render(request, 'knn.html', {
            'type_of_food_options': type_of_food_options,
            'event_type_options': event_type_options,
            'storage_conditions_options': storage_conditions_options,
            'prediction_text': f'Predicted Number Fed: {predicted_number_fed}'
        })

    except Exception as e:
        return render(request, 'knn.html', {
            'type_of_food_options': type_of_food_options,
            'event_type_options': event_type_options,
            'storage_conditions_options': storage_conditions_options,
            'error_text': f'Error: {str(e)}'
        })

def api_predict(request):
    try:
        data = json.loads(request.body)

        # Extract and encode the input data
        encoded_type_of_food = label_encoders['Type of Food'].transform([data['type_of_food']])[0]
        quantity = float(data['quantity'])
        encoded_event_type = label_encoders['Event Type'].transform([data['event_type']])[0]
        encoded_storage_conditions = label_encoders['Storage Conditions'].transform([data['storage_conditions']])[0]

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        # Prepare input data
        input_data = pd.DataFrame({
            'Type of Food': [encoded_type_of_food],
            'Quantity of food': [quantity],
            'Event Type': [encoded_event_type],
            'Storage Conditions': [encoded_storage_conditions]
        })

        # Scale input
        scaled_input = scaler.transform(input_data)

        # Predict
        prediction = model.predict(scaled_input)
        predicted_number_fed = round(prediction[0], 2)
        if predicted_number_fed < 0:
            predicted_number_fed = 0

        return JsonResponse({'predicted_number_fed': predicted_number_fed})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)