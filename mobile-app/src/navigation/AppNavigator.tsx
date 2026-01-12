import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import FaceRecognitionScreen from '../screens/FaceRecognitionScreen';

const Stack = createNativeStackNavigator();

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
        }}
      >
        <Stack.Screen name="FaceRecognition" component={FaceRecognitionScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

