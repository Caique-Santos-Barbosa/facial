import { useState, useEffect } from 'react';
import { Camera, useCameraDevice } from 'react-native-vision-camera';
import { useIsFocused } from '@react-navigation/native';

export function useCamera() {
  const [hasPermission, setHasPermission] = useState(false);
  const device = useCameraDevice('front');
  const isFocused = useIsFocused();

  useEffect(() => {
    (async () => {
      const status = await Camera.requestCameraPermission();
      setHasPermission(status === 'granted');
    })();
  }, []);

  return {
    device,
    hasPermission,
    isActive: hasPermission && isFocused && device != null,
  };
}

