import React,{useState} from 'react'
import PasswordChecklist from 'react-password-checklist'

const Login = () => {

    const [signUp, setSignUp] = useState(false)
    const [isPasswordValid, setIsPasswordValid] = useState(false)
    const [authInfo, setAuthInfo] = useState({
        email:"",
        password:"",
        confirmPassword:""
    })

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
                            <button type='submit' onClick={()=>{alert(JSON.stringify(authInfo))}} className='text-white bg-green-700 w-1/2 m-auto p-1'>Sign Up</button>
                        )
                        :(
                            <button type='submit' className='text-white bg-green-700 w-1/2 m-auto p-1'>Sign In</button>
                        )
                    }
                    <button type='submit' className='text-white bg-green-700 w-1/2 m-auto p-1'>Sign In with Google</button>
                    <p className='w-1/2 m-auto text-center cursor-pointer text-blue-600' onClick={changePageLayout}>{
                        signUp ? "Already have an account?" : "Create a new account."
                    }</p>

                </form>
            </div>
        </div>
    )
    }

export default Login