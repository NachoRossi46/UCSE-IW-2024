import {
  BanknotesIcon,
  ClockIcon,
  UserGroupIcon,
  InboxIcon,
} from '@heroicons/react/24/outline';
import { lusitana } from '@/components/ui/fonts';
import Link from 'next/link';
import Image from 'next/image';
import AcmeLogo from '../acme-logo';

const iconMap = {
  collected: BanknotesIcon,
  customers: UserGroupIcon,
  pending: ClockIcon,
  invoices: InboxIcon,
};

interface CardWrapperProps {
  totalPendingInvoices: string;
  totalPaidInvoices: string;
  numberOfInvoices: number;
  numberOfCustomers: number;
}

export default async function CardWrapper({ numberOfCustomers, numberOfInvoices, totalPaidInvoices, totalPendingInvoices }: CardWrapperProps) {
  return (
    <>
      {/* NOTE: Uncomment this code in Chapter 9 */}

      <Card title="Collected" value={totalPaidInvoices} type="collected" />
      <Card title="Pending" value={totalPendingInvoices} type="pending" />
      <Card title="Total Invoices" value={numberOfInvoices} type="invoices" />
      <Card
        title="Total Customers"
        value={numberOfCustomers}
        type="customers"
      />
    </>
  );
}

export function Card({
  title,
  value,
  type,
}: {
  title: string;
  value: number | string;
  type: 'invoices' | 'customers' | 'pending' | 'collected';
}) {
  const Icon = iconMap[type];

  return (

    <div className="rounded-xl bg-gray-200 p-2 shadow-sm">
      <div className="flex p-4">
        {Icon ? <Icon className="h-5 w-5 text-gray-700" /> : null}
        <h3 className="ml-2 text-sm font-medium">{title}</h3>
      </div>
      <p
        className={`${lusitana.className}
          truncate rounded-xl bg-white px-4 py-8 text-center text-2xl`}
      >
        {value}
      </p>
    </div>
  );
}

//Chanchada 
interface CardBgProps {
  classNamesDivLogo?: string;
  classNamesLink?: string;
  classNamesImg?: string;
  img: string;
  alt: string;
}

export function CardWithBackground({ classNamesDivLogo, img, alt }: CardBgProps) {
  return (
    <div>
      <Link
        className="relative mb-2 flex h-20 items-end justify-start rounded-md overflow-hidden md:h-40"
        href="/"
      >
        <Image
          src={img} // Asegúrate de que esta ruta sea correcta
          alt={alt}
          layout="fill"
          objectFit="cover"
          className="absolute inset-0 z-0 opacity-70" // Ajusta la opacidad según sea necesario
          quality={100}
        />
        <div className={`${ classNamesDivLogo ? classNamesDivLogo : "w-32 text-white md:w-40 z-10 relative"}`}>
          <AcmeLogo />
        </div>
      </Link>
    </div>
  )
}
