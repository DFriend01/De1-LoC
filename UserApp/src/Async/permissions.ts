/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import { Camera } from "react-native-vision-camera"

const getCameraPermission = async () => {
    await Camera.requestCameraPermission();
}

export default getCameraPermission;