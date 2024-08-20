import React, { useState } from "react";
import { lusitana } from "../ui/fonts";
import Cookies from "js-cookie";
import {
  ArrowRightIcon,
  AtSymbolIcon,
  KeyIcon,
  FaceSmileIcon,
  FaceFrownIcon
} from "@heroicons/react/24/outline";
import { Button } from "../ui/button";
import { Controller, useForm } from "react-hook-form";
import * as yup from "yup";
import { useMutation } from "react-query";
import { yupResolver } from "@hookform/resolvers/yup";
import { TextField } from "@mui/material";

interface SignupFormProps {
  onSignupSuccess: () => void;
}

interface SignupFormData {
  email: string;
  nombre: string;
  apellido: string;
  password: string;
  confirmPassword: string;
}

const schema = yup.object().shape({
  email: yup.string().email("Email no valido").required("Email es obligatorio"),
  nombre: yup.string().required("El nombre es obligatorio"),
  apellido: yup.string().required("El apellido es obligatorio"),
  password: yup
    .string()
    .min(8, "La contraseña debe tener mínimo 8 caracteres.")
    .required("La contraseña es obligatoria"),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref("password"), ""], "Las contraseñas deben coincidir")
    .required("Debes confirmar la nueva contraseña.")
    // .min(8, "La contraseña debe tener mínimo 8 caracteres."),
});

const SignupForm: React.FC<SignupFormProps> = ({ onSignupSuccess }) => {
  const {
    register,
    control,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<SignupFormData>({
    resolver: yupResolver(schema),
  });

  const signupMutation = useMutation(
    ({ email, nombre, apellido, password }: SignupFormData) =>
      fetch(`${process.env.NEXT_PUBLIC_API_ENDPOINT}/auth/registro/`, {
        // fetch(`http://localhost:8000/auth/registro/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, nombre, apellido, password, rol: 4 }),
      }).then((response) => {
        if (!response.ok) {
          throw new Error("Signup failed");
        }
        return response.json();
      }),
    {
      onSuccess: (data) => {
        Cookies.set("token", data.token, { expires: 1 });
        onSignupSuccess();
      },
      onError: (error) => {
        console.error("Error:", error);
      },
    }
  );

  const onSubmit = (data: SignupFormData) => {
    if (data.password !== data.confirmPassword) {
      setError("confirmPassword", {
        type: "manual",
        message: "Las contraseñas no coinciden",
      });
      return;
    }

    // Si las contraseñas coinciden, procede con el registro
    signupMutation.mutate(data);
  };

  return (
    <form className="space-y-3" onSubmit={handleSubmit(onSubmit)}>
      <div className="flex-1 rounded-lg bg-gray-50 px-6 pb-4 pt-8">
        <h1 className={`${lusitana.className} mb-3 text-2xl`}>
          Registrese para poder ingresar.
        </h1>
        <div className="w-full">
          <div>
            <label
              className="mb-3 mt-5 block text-xs font-medium text-gray-900"
              htmlFor="email"
            >
              Email
            </label>
            <div className="relative">
              <input
                className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
                id="email"
                type="email"
                {...register("email")}
                placeholder="Ingrese su email"
              />
              <AtSymbolIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
            </div>
            {errors.email && (
              <p className="text-red-500 text-xs mt-1">
                {errors.email.message}
              </p>
            )}
          </div>
          <div className="mt-4">
            <label
              className="mb-3 mt-5 block text-xs font-medium text-gray-900"
              htmlFor="name"
            >
              Nombre
            </label>
            <div className="relative">
              <input
                className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
                id="name"
                type="text"
                {...register("nombre")}
                placeholder="Ingrese su nombre"
              />
              <FaceSmileIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
            </div>
            {errors.nombre && (
              <p className="text-red-500 text-xs mt-1">{errors.nombre.message}</p>
            )}
          </div>
          <div className="mt-4">
            <label
              className="mb-3 mt-5 block text-xs font-medium text-gray-900"
              htmlFor="lastName"
            >
              Apellido
            </label>
            <div className="relative">
              <input
                className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
                id="lastName"
                type="text"
                {...register("apellido")}
                placeholder="Ingrese su apellido"
              />
              <FaceSmileIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
            </div>
            {errors.apellido && (
              <p className="text-red-500 text-xs mt-1">
                {errors.apellido.message}
              </p>
            )}
          </div>
          <div className="mt-4">
            <label
              className="mb-3 mt-5 block text-xs font-medium text-gray-900"
              htmlFor="password"
            >
              Contraseña
            </label>
            <div className="relative">
              <input
                className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
                id="password"
                type="password"
                {...register("password")}
                placeholder="Contraseña"
              />
              <KeyIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
            </div>
            {errors.password && (
              <p className="text-red-500 text-xs mt-1">
                {errors.password.message}
              </p>
            )}
          </div>
          <Controller
            defaultValue=""
            name="confirmPassword"
            control={control}
            render={({ field }) => (
              <div className="mt-4">
                <label
                  className="mb-3 mt-5 block text-xs font-medium text-gray-900"
                  htmlFor="password"
                >
                  Repita su contraseña
                </label>
                <div className="relative">
                  <input
                    className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
                    id="repeat-password"
                    type="password"
                    {...register("confirmPassword")}
                    placeholder="Contraseña"
                  />
                  <KeyIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
                </div>
                {errors.confirmPassword && (
                  <p className="text-red-500 text-xs mt-1">
                    {errors.confirmPassword.message}
                  </p>
                )}
              </div>
            )}
          />
        </div>
        <Button
          className="mt-4 w-full"
          type="submit"
          disabled={signupMutation.isLoading}
        >
          {signupMutation.isLoading ? "Signing up..." : "Sign up"}{" "}
          <ArrowRightIcon className="ml-auto h-5 w-5 text-gray-50" />
        </Button>
        {signupMutation.isError && (
          <p className="text-red-500 text-sm mt-2">
            An error occurred during signup. Please try again.
          </p>
        )}
      </div>
    </form>
  );
};

export default SignupForm;
