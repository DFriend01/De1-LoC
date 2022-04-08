/* Relative Imports */
import { CodeObject } from "../Screens/CodeManagement/CodeListItem";
import { URL } from '../utils/config'

const apiURL: string = `${URL}code`;

export const editCode = async (
    data: CodeObject,
    onSuccess: () => void,
    onFailure: (e: string) => void
) => {
    await fetch(
        apiURL + '/modify',
        {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
    ).then(
        (response) => {
            if (response.status == 200) {
                onSuccess();
            } 
            return response.json();
        }
    ).then(
        (json) => {
            if (json.message != undefined){
                onFailure(json.message);
            }
        }
    )
}

export const deleteCode = async (
    id: number,
    onSuccess: () => void,
    onFailure: (e: string) => void
) => {
    await fetch(
        apiURL + "/delete",
        {
            method: 'DELETE',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id
            })
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
            if(json.message != undefined) {
                onFailure(json.message);
            }
        }
    )
 }

export const createCode = async (
    data: CodeObject,
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
                code: data.code,
                codename: data.codename
            })
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
            if(json.message != undefined)
                onFailure(json.message);
        }
    )
}