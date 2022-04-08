/* Relative Imports */
import { URL } from '../utils/config';

const apiURL : string = URL;

export const authFaceID = async (
    file: string,
    onSuccess: () => void,
    onFailure: (e : string) => void
) => {
    const data = new FormData();
    data.append('file', {
        uri: file,
        type: 'image/jpg',
        name: 'face.jpg'
    });
    await fetch(
        apiURL + "auth/face",
        {
            method: "POST",
            headers: {
                Accept: 'application/json',
                'Content-Type': 'multipart/form-data'
            },
            body: data
        }
    ).then((response) => response.json()).then(
        (json) => {
            if (json.message == undefined) {
                onSuccess();
            } else {
                console.log(json.message);
                onFailure(json.message);
            }
        }
    )
}

export const registerFace = async (
    files: string[],
    onSuccess: () => void,
    onFailure: () => void
) => {
    const data = new FormData();
    files.map((file, index) => {
        /*
         * from flavioscopes.com/how-to-get-last-item-path-javascript/
         */
        const name = file.substring(file.lastIndexOf('/')+1)
        data.append("name", name);
        data.append("p"+index, {
            uri: file,
            type: "image/jpg",
            name: name
        })
    });
    await fetch(
        apiURL + "user/reguserface",
        {
            method: "POST",
            headers: {
                Accept: 'application/json',
                'Content-Type': 'multipart/form-data'
            },
            body: data
        }
    ).then((response) => response.json()).then(
        (json) => {
            if (json.message == undefined) {
                console.log(json);
                onSuccess();
            } else {
                console.log(json.mesage);
                onFailure();
            }
        }
    )
}