/* Relative Imports */
import { URL } from '../utils/config';

const apiURL : string = `${URL}user`;

export interface userData {
    username: string,
    firstname: string,
    lastname: string,
    password: string
};
export interface result {
    success: boolean;
    error: string;
}
export interface ReturnedProfileData {
    username: string;
    firstname: string;
    lastname: string;
    face_enabled: number;
}

export const getProfile = async (
    onSuccess: (data: ReturnedProfileData) => void,
    onFailure: (e: string) => void,
) => {
    await fetch(
        apiURL + "/profile",
        {
            method: "GET",
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        }
    ).then(
        (response) => {
            return response.json();
        }
    ).then(
        (json) => {
            if(json.message == undefined){
                console.log(json);
                onSuccess(json);
            } else {
                onFailure(json.message);
            }
        }
    )
}

export const getCodes = async (
    onSuccess: (code: Object) => void,
    onFailure: (e: string) => void
) => {
    await fetch(
        apiURL + "/codes",
        {
            method: "GET",
            headers: {
                Accept: 'application/json',
                'Content-Type':'application/json'
            }
        }
    ).then(
        (response) => response.json()
    ).then(
        (json) => {
            if (json.message == undefined) {
                onSuccess(json);
            } else {
                onFailure(json.message);
            }
        }
    )
}

export const userRegister = async (
    data: userData,
    onSuccess: () => void,
    onFailure: (e: string) => void
) => {
    await fetch(
        apiURL + "/register",
        {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: data.username,
                firstname: data.firstname, 
                lastname: data.lastname,
                password: data.password
            })
            
        }
    ).then(
        (response) => {
            if(response.status == 200){
                onSuccess();
            }
            return response.json();
        }
    ).then(
        (json) => {
            if(json.message != undefined)
                onFailure(json.message);
        }
    )
}

