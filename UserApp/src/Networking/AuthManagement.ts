/* Relative Imports */
import {URL} from '../utils/config';

const apiURL : string = `${URL}auth`

interface AuthData {
    username: string;
    password: string;
    token: string;
};

export const unlock = async (
    code: string,
    onSuccess: () => void,
    onFailure: (e: string) => void
) => {
    await fetch(
        apiURL + "/code",
        {
            method: "POST",
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body:JSON.stringify({code})
        }
    ).then(
        (response) => {
            if(response.status == 200) {
                onSuccess();
            }
            return response.json();
        }
    ).then(
        (json) => {
            if(json.message != undefined){
                onFailure(json.message);
            }
        }
    )
}

export const login = async (
    data: AuthData,
    onSuccess: () => void,
    onFailure: (e: string) => void
) => {
    await fetch(
        apiURL + "/login",
        {
            method: "POST",
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
    ).then(
        (response) => {
            if(response.status == 200) {
                console.log(response)
                onSuccess();
            }
            return response.json();
        }, 
        (e: string) => console.log(e)
    ).then(
        (json) => {
            console.log(json)
            if(json.message != undefined)
                onFailure(json.message);
        },
        (e: string) => console.log(e)
    )
}

export const logout = async (
    onSuccess: () => void,
    onFailure: (e: string) => void
) => {
    await fetch(
        apiURL + '/logout',
        {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
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
            if(json.message != undefined) {
                onFailure(json.message);
            }
        }
    )
}