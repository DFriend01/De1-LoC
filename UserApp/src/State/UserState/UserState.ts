/* Relative Imports */
import { CodeObject } from "../../Screens/CodeManagement/CodeListItem";

export interface UserState {
    codes: CodeObject[];
    profile: Profile;
    logs: Log[];
    logOffset: number,
}

export interface Log {
    success: number,
    user_id: number,
    username: string,
    codename: string,
    verifDate: string,
    verifTime: string
};
export interface Profile {
    firstname: string;
    lastname: string;
    username: string;
    face_enabled: number;
}
 export const initialUser : UserState = {
    codes:[],
    profile: {
        firstname:"",
        lastname: "",
        username: "",
        face_enabled: 0
    },
    logs: [],
    logOffset: 0
 }