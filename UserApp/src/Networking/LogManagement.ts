/* Relative Imports */
import { URL } from '../utils/config'

const apiURL : string =`${URL}log/query`;


export const getNextLogs = async (
    offset : number,
    onSuccess : (data: any) => void,
    onFailure : (e:string) => void,
) => {
    await fetch(
        apiURL + `?nlogs=5&offset=${offset}`,
        {
            method: "GET",
            headers: {
                Accept: 'application/json',
                'Content-Type' : 'application/json'
            }
        }
    ).then(
        (response) => {
            return response.json()
        }
    ).then(
        (json) => {
            if (json.message == undefined) {
                onSuccess(json);
            } else {
                onFailure(json.message)
            }
        }
    )
}

export const getLogs = async (
    onSuccess: (data: any) => void,
    onFailure: (e: string) => void
) => {
    await fetch(
        apiURL+"?nlogs=5",
        {
            method: "GET",
            headers: {
                Accept: 'application/json',
                'Content-Type' : 'application/json'
            }
        }
    ).then(
        (response) => {
            return response.json()
        }
    ).then(
        (json) => {
            if(json.message == undefined){
                onSuccess(json);
            }else {
                onFailure(json.message);
            }
        }
    )
};