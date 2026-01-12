import AsyncStorage from '@react-native-async-storage/async-storage';

const STORAGE_KEYS = {
  DEVICE_ID: 'device_id',
  LAST_RECOGNITION: 'last_recognition',
};

export async function getDeviceId(): Promise<string> {
  let deviceId = await AsyncStorage.getItem(STORAGE_KEYS.DEVICE_ID);
  
  if (!deviceId) {
    deviceId = `device_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    await AsyncStorage.setItem(STORAGE_KEYS.DEVICE_ID, deviceId);
  }
  
  return deviceId;
}

export async function saveLastRecognition(data: any): Promise<void> {
  await AsyncStorage.setItem(STORAGE_KEYS.LAST_RECOGNITION, JSON.stringify(data));
}

export async function getLastRecognition(): Promise<any | null> {
  const data = await AsyncStorage.getItem(STORAGE_KEYS.LAST_RECOGNITION);
  return data ? JSON.parse(data) : null;
}

