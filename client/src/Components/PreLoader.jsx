import React, {useEffect} from 'react'
import { preLoaderAnim } from '../utils/preLoaderAnim'
import './PreLoader.css'

const PreLoader = () => {

    useEffect(()=> {
        preLoaderAnim()
    }, []);
    
    return (
        <div className="preloader">
            <div className="texts-container">
                <span>Welcome to the brain signal reader!</span>
            </div>
        </div>

    )
}

export default PreLoader 