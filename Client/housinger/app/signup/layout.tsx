"use client";

import { useAuthStore } from "@/store/auth/auth.store";
import { useRouter } from "next/navigation";
import { ReactNode } from "react";

export const SignupLayout = ({ children }: { children: ReactNode }) => {
  const router = useRouter();
  const authStatus = useAuthStore((state) => state.status);
  const checkAuthStatus = useAuthStore((state) => state.checkAuthStatus);

  if (authStatus === "Pending") {
    checkAuthStatus();
    return <div>Loading...</div>;
  }

  if (authStatus === "Authorized") router.push("/dashboard");

  return (
    <div className="bg-gray-100 flex justify-center items-center h-screen">
      <div className="w-1/2 h-screen hidden lg:flex lg:flex-col items-center justify-center bg-indigo-700">
        {/* <div className="pixels-photo">
          <a
            href="https://500px.com/photo/77888323/living-by-arild-aarnes"
            id="Living by Arild Aarnes on 500px.com"
          >
            <img
              src="https://drscdn.500px.org/photo/77888323/q%3D80_m%3D600/v2?sig=cd5b26acda59ddcc45082c69beb4e7dbe4ea79e316a971f3e0cc82a195da11f7"
              alt="Living by Arild Aarnes on 500px.com"
            />
          </a>
        </div>

        <script
          type="text/javascript"
          src="https://500px.com/embed.js"
        ></script> */}
        {/* <span className="text-white font-bold text-9xl">Zustand</span> */}
        <img
          src="./frontb&w.jpg"
          alt="Placeholder Image"
          className="object-cover w-full h-full"
        />
      </div>
      <div className="lg:p-36 md:p-52 sm:20 p-8 w-full lg:w-1/2">
        {children}
      </div>
    </div>
  );
};

export default SignupLayout;
