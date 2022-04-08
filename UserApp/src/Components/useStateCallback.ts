/**
 * Wrapper for useState that allows it to be used with callbacks. Code from:
 * https://stackoverflow.com/questions/54954091/how-to-use-callback-with-usestate-hook-in-react/61842546#61842546
 * Code Modified to work with TypeScript 
**/

/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import { useState, useRef, useCallback, useEffect } from 'react';

export type Callback = (s?: any) => any;
export type SetStateCallback = (s: any, cb?: any) => void;
function useStateCallback(initialState: any) {
    const [state, setState] = useState(initialState);
    const cbRef = useRef(null); // init mutable ref container for callbacks
  
    const setStateCallback : SetStateCallback = useCallback((state, cb) => {
      cbRef.current = cb; // store current, passed callback in ref
      setState(state);
    }, []); // keep object reference stable, exactly like `useState`
  
    useEffect(() => {
      // cb.current is `null` on initial render, 
      // so we only invoke callback on state *updates*
      if (cbRef.current) {
        const callback = cbRef.current as Callback
        callback(state)
        // cbRef.current(state);
        cbRef.current = null; // reset callback after execution
      }
    }, [state]);
  
    return [state, setStateCallback];
  }

export default useStateCallback;