import React, { useState } from 'react';
import { StatusBar } from 'react-native';
import SplashScreen from './src/screens/SplashScreen';
import FaceRecognitionScreen from './src/screens/FaceRecognitionScreen';

export default function App() {
  const [showSplash, setShowSplash] = useState(true);

  if (showSplash) {
    return <SplashScreen onFinish={() => setShowSplash(false)} />;
  }

  return (
    <>
      <StatusBar barStyle="light" />
      <FaceRecognitionScreen />
    </>
  );
}
