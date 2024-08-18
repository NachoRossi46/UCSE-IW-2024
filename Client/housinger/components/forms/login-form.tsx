"use client";

import { lusitana } from "@/components/ui/fonts";
import {
  AtSymbolIcon,
  KeyIcon,
  ExclamationCircleIcon,
} from "@heroicons/react/24/outline";
import { ArrowRightIcon } from "@heroicons/react/20/solid";
import { Button } from "../ui/button";
import * as Yup from "yup";
import { Controller, Field, useForm } from "react-hook-form";
// import { authenticate } from "@/app/lib/actions";
import { FormEvent, useActionState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth/auth.store";

interface LoginFormInput {
  mail: string;
  nombre: string;
  nroContacto: number;
  contraseña?: string | null;
}

const defaultValues: LoginFormInput = {
  mail: '',
  nombre: '',
  nroContacto: 0,
  contraseña: ''
}

const schema = Yup.object<LoginFormInput>().shape({
  mail: Yup.string().required('Debe ingresar un mail').email('Debe ingresar un email valido'),
  contraseña: Yup.string()
      .nullable()
      .test('contraseña', 'La contraseña debe tener entre 8 y 20 caracteres.', function (value) {
        // if (!!value || !isEditing) {
          const schema = Yup.string().min(8).max(20);
          return schema.isValidSync(value);
        // }
        // return true;
      }),
  nombre: Yup.string().required('Ingrese un nombre y apellido'),
  nroContacto: Yup.number().max(16, 'No puede contener mas de 16 numeros')
})

export const LoginForm: React.FC = () => {
  // const [errorMessage, formAction, isPending] = useActionState(
  //   authenticate,
  //   undefined
  // );
  const router = useRouter();

  const loginUser = useAuthStore((state) => state.loginUser);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    // const { username, password, remember } = event.target as HTMLFormElement;
    const { username, password, remember } =
      event.target as typeof event.target & {
        username: { value: string };
        password: { value: string };
        remember: { checked: boolean };
      };
    console.log(username.value, password.value, remember.checked);
    try {
      await loginUser(username.value, password.value);
      router.push("/dashboard");
    } catch (error) {
      console.log("No se pudo autenticar");
    }

    // username.value = '';
    // password.value = '';
    // remember.checked = false;
  };

  return (
    // <form action={formAction} className="space-y-3">
    <form className="space-y-3">
      <div className="flex-1 rounded-lg bg-gray-50 px-6 pb-4 pt-8">
        <h1 className={`${lusitana.className} mb-3 text-2xl`}>
          Please log in to continue.
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
                name="email"
                placeholder="Enter your email address"
                required
              />
              <AtSymbolIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
            </div>
          </div>
          <div className="mt-4">
            <label
              className="mb-3 mt-5 block text-xs font-medium text-gray-900"
              htmlFor="password"
            >
              Password
            </label>
            <div className="relative">
              <input
                className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
                id="password"
                type="password"
                name="password"
                placeholder="Enter password"
                required
                minLength={6}
              />
              <KeyIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
            </div>
          </div>
        </div>
        {/* <Button aria-disabled={isPending} className="mt-4 w-full"> */}
        <Button className="mt-4 w-full">
          Log in <ArrowRightIcon className="ml-auto h-5 w-5 text-gray-50" />
        </Button>
        <div className="flex h-8 items-end space-x-1">
          {/* {errorMessage && (
            <>
              <ExclamationCircleIcon className="h-5 w-5 text-red-500" />
              <p className="text-sm text-red-500">{errorMessage}</p>
            </>
          )} */}
        </div>
      </div>
    </form>
  );
}
