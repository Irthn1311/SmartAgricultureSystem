import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import joblib
import pandas as pd
from datetime import datetime, timedelta

def preprocess_data(df):
    # Chuyển đổi RainToday
    df['RainToday'] = df['RainToday'].map({'Yes': 1, 'No': 0})
    
    # Xử lý missing values
    df.dropna(inplace=True)
    
    # Chọn features
    features = ['MinTemp', 'MaxTemp', 'Humidity', 'Cloud', 'Temp', 'RainToday']
    
    return df[features]

try:
    # Load scaler và model
    scaler = joblib.load("scaler.save")
    model = load_model("weather_model.keras")
    
    # Load và tiền xử lý dữ liệu
    df = pd.read_csv("Weather_Data.csv")
    features = preprocess_data(df)
    
    # Chuẩn hóa dữ liệu
    scaled_features = scaler.transform(features)
    
    # Lấy 3 ngày cuối cùng
    X_input = scaled_features[-3:]
    X_input = X_input.reshape((1, 3, 6))
    
    # Dự đoán
    predictions = model.predict(X_input)[0]
    
    # Hiển thị kết quả
    print("\n🌤️ Dự đoán thời tiết cho 3 ngày tới:")
    print("=" * 50)
    
    for i, day in enumerate(predictions):
        # Tính ngày
        current_date = datetime.now() + timedelta(days=i+1)
        date_str = current_date.strftime("%d/%m/%Y")
        
        # Lấy xác suất
        prob_rain = day[1] * 100
        prob_no_rain = day[0] * 100
        
        # Quyết định
        will_rain = np.argmax(day) == 1
        
        print(f"\n📅 Ngày {date_str}:")
        print(f"   - Xác suất mưa: {prob_rain:.1f}%")
        print(f"   - Xác suất không mưa: {prob_no_rain:.1f}%")
        print(f"   - Dự đoán: {'Có mưa' if will_rain else 'Không mưa'}")
    
except FileNotFoundError as e:
    print(f"❌ Lỗi: Không tìm thấy file {str(e)}")
except Exception as e:
    print(f"❌ Lỗi: {str(e)}")
