/* Relative Imports */
import { ERROR } from '../../utils/errors';
/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import * as Yup from 'yup';


export const DoorCodeSchema = Yup.object().shape({
    codename: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    doorcode: Yup.string().length(4, ERROR.mustBeFour).required(ERROR.required)
})
export const EditCodeSchema = Yup.object().shape({
    codename: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    code: Yup.string().length(4, ERROR.mustBeFour).required(ERROR.required)
})