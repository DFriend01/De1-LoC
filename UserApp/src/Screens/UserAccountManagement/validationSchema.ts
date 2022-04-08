/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import * as Yup from 'yup';
/* Relative Imports */
import { ERROR } from '../../utils/errors';

export const RegistrationSchema = Yup.object().shape({
    firstname: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    lastname: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    username: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    password: Yup.string().min(8, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    confirmPass: Yup.string().required(ERROR.required).oneOf([Yup.ref('password')], ERROR.mustMatch)
});

export const LoginSchema = Yup.object().shape({
    username: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    password: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required)
});