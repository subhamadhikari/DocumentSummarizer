import React,{useState} from 'react'
import PasswordChecklist from 'react-password-checklist'
import { signup,signin } from '../../api/auth'
import { useNavigate } from 'react-router-dom'
import { useEffect } from 'react'
import { jwtDecode } from "jwt-decode";
import Popup from '../components/Popup'

const Login = () => {

    const [signUp, setSignUp] = useState(false)
    const [isPasswordValid, setIsPasswordValid] = useState(false)
    const [authInfo, setAuthInfo] = useState({
        email:"",
        password:"",
        confirmPassword:""
    })
    const [status, setStatus] = useState({
        status_code:200,
        status_message:""
    })

    const navigate = useNavigate()

    const handleChange = (event) => {
        const value = event.target.value
        setAuthInfo({
            ...authInfo,
            [event.target.name]:value
        })
        if(isPasswordValid == true && (event.target.name == "confirmPassword" || event.target.name == "password")){
            setIsPasswordValid(false)
        }
    }

    const changePageLayout = () => {
        setSignUp((prev) => !prev)
    }

    const register = async() =>{
        if(!isPasswordValid){
            alert("Password requirement is not fulfilled!")
            return
        }
        const response = await signup({email:authInfo.email,password:authInfo.password})
        console.log(response)
    }

    const login = async(e) => {
        e.preventDefault()
        const response = await signin({email:authInfo.email,password:authInfo.password})
        // const data = await response.json()

        console.log("in response::",response)
        setStatus({status_code:response.status,status_message:response.detail})

        if(response.status_code == 200){
            navigate("/")
        }
        console.log(response)
    }

    const isTokenExpired = (token) => {
        try {
            const decoded = jwtDecode(token)
            const currentTime = Date.now() / 1000
            return decoded.exp < currentTime
        } catch (error) {
            return true
        }
    }

    useEffect(() => {
        let token = localStorage.getItem("token")
        if(token && token !== null){
            const tokenExpired = isTokenExpired(token)
            if(tokenExpired){
                localStorage.removeItem("token")
            }else{
                navigate("/")
            }
        }
    }, [])
    

    return (
        <div className='bg-slate-800 h-screen p-6 flex justify-center items-center'>
            <div className='bg-[#c9c7e7] h-3/4 w-1/2 rounded-lg'>
                <form className='flex flex-col justify-start items-start h-full w-full p-4'>
                    <h1 className='font-bold text-black w-1/2 m-auto text-center text-3xl'>{
                        signUp ? "Sign Up" : "Sign In"
                    }</h1>
                    <label className='text-black w-1/2 m-auto'>Email</label>
                    <input name='email' onChange={handleChange} className='text-black w-1/2 m-auto rounded-lg focus:outline-none focus:ring-purple-400 focus:ring-1 focus:border-purple-600 p-2.5 bg-gray-50 border border-gray-300' type='email' placeholder='Enter e-mail'/>
                    <label className='text-black w-1/2 m-auto'>Password</label>
                    <input name='password' onChange={handleChange} className='text-black w-1/2 m-auto rounded-lg focus:outline-none focus:ring-purple-400 focus:ring-1 focus:border-purple-600 p-2.5 bg-gray-50 border border-gray-300' type='password' placeholder='Enter password'/>
                    {/* <p class="mt-2 text-sm text-red-600 dark:text-red-500"><span class="font-medium">Oops!</span> Username already taken!</p> */}
                    {
                    signUp && (
                    <>
                        <label className='text-black w-1/2 m-auto'>Confirm Password</label>
                        <input name="confirmPassword" onChange={handleChange} className='text-black w-1/2 m-auto rounded-lg focus:outline-none focus:ring-purple-400 focus:ring-1 focus:border-purple-600 p-2.5 bg-gray-50 border border-gray-300' type='password' placeholder='Re-enter password'/>
                        {
                            !isPasswordValid && (
                                <PasswordChecklist rules={["minLength","specialChar","match"]}
                                minLength={8}
                                value={authInfo.password}
                                valueAgain={authInfo.confirmPassword}
                                style={{margin:"auto",width:"50%",color:"red !Important"}}
                                className='checklist'
                                onChange={(isValid,failedRules)=>{
                                    setIsPasswordValid(isValid)
                                }}
                                messages={{
                                    minLength: "Enter atleast 8 characters",
                                    specialChar: "Provide at least one special character",
                                    match: "Passwords in the field mismatch.",
                                }}
                            />
                            )
                        }
                    </>
                    )
                    }

                    {
                        signUp ? 
                        (
                            <button type='submit' onClick={register} className='text-white bg-green-700 w-1/2 m-auto p-1'>Sign Up</button>
                        )
                        :(
                            <button type='submit' onClick={login} className='text-white bg-green-700 w-1/2 m-auto p-1'>Sign In</button>
                        )
                    }
                    <button type='submit' className='text-white bg-green-700 w-1/2 m-auto p-1'>Sign In with Google</button>
                    <p className='w-1/2 m-auto text-center cursor-pointer text-blue-600' onClick={changePageLayout}>{
                        signUp ? "Already have an account?" : "Create a new account."
                    }</p>

                </form>
            </div>

            {status.status_code !== 200 && (
                <Popup message={status.status_message}/>
            )}
        </div>
    )
    }


export default Login