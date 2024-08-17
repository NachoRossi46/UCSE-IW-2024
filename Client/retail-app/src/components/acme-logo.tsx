import { GlobeAltIcon } from '@heroicons/react/24/outline';

export default function AcmeLogo() {
  return (
    <div >
      {/*<Image
        src="/cat.png" // Asegúrate de que esta ruta sea correcta
        alt="Logo for Background"
        layout="fill"
        objectFit="cover"
        className="absolute inset-0 z-0 opacity-70" // Ajusta la opacidad según sea necesario
        quality={100}
  />*/}
      <div
        className={`flex flex-row items-center leading-none text-white`}
      >
        <GlobeAltIcon className="h-12 w-12 rotate-[15deg]" />
        <p className="text-[44px]">Housinger</p>
      </div>
    </div>
  );
}


{/*<Image 
        src={'/cat.png'}
        alt='Logo for Background'
        layout='fill'
        objectFit='cover'
        className='opacity-70'
        quality={100}
      />*/}