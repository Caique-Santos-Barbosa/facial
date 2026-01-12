import { FaceDetector } from '@react-native-ml-kit/face-detection';

const faceDetector = FaceDetector.faceDetector({
  enableClassification: false,
  enableLandmarks: false,
  enableTracking: false,
  minFaceSize: 0.15,
  performanceMode: 'fast',
});

export interface FaceDetectionResult {
  hasFace: boolean;
  faceCount: number;
}

export async function detectFaceInImage(imagePath: string): Promise<FaceDetectionResult> {
  try {
    const faces = await faceDetector.processImage(imagePath);
    return {
      hasFace: faces.length > 0,
      faceCount: faces.length,
    };
  } catch (error) {
    console.error('Face detection error:', error);
    return {
      hasFace: false,
      faceCount: 0,
    };
  }
}

