import React, { useRef, useState } from 'react';
import logo from "../assets/logo.png";
import { IoIosAddCircleOutline } from "react-icons/io";
import axios from 'axios';
import { toast } from 'react-toastify';
import { ThreeDots } from 'react-loader-spinner'
import pdfIcon from "../assets/file-icon.png";


const Navbar = ({ pdf, setPdf }) => {
    const fileInputRef = useRef(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = async (event) => {
        const file = event.target.files[0];
        if (file) {
            // Checking if the file is a PDF file or not
            if (file.type !== 'application/pdf') {
                toast.error('Please upload a PDF file', {
                    position: "top-center",
                    autoClose: 3000,
                });
                return;
            }
            try {

                setLoading(true);
                const formData = new FormData();
                formData.append('pdf_document', file);
                const response = await axios.post('/pdf-upload/', formData);
                console.log(response);

                if (response.status === 200) {
                    setPdf(response.data);
                    toast.success('PDF File uploaded successfully', {
                        position: "top-center",
                        autoClose: 3000,
                    });
                } else {
                    throw new Error('Error uploading file');
                }
            } catch (error) {
                console.log(error);
                toast.error('Error uploading file, Please Try again in some time', {
                    position: "top-center",
                    autoClose: 3000,
                });
            } finally {
                setLoading(false);
            }
        }
    };

    const handleUploadClick = () => {
        fileInputRef.current.click();
    };

    return (
        <div className='fixed top-0 bg-white w-full flex py-5  justify-between shadow-[0px_-8px_25px_0px_rgba(0,0,0,0.22)]  px-[2.5%] sm:px-10 lg:px-20'>
            <div>
                <img src={logo} alt="Ai planet Logo" />
            </div>
            <div>
                <input
                    type="file"
                    ref={fileInputRef}
                    style={{ display: 'none' }}
                    accept="application/pdf"
                    onChange={handleFileChange}
                />
                {loading ?
                    <ThreeDots
                        height={40}
                        width={80}
                        color="#0FA958"
                        ariaLabel="three-dots-loading"
                        wrapperStyle={{}}
                        wrapperClass=""
                    /> :
                    <PdfUploadButn handleUploadClick={handleUploadClick} pdf={pdf} />
                }
            </div>
        </div >
    );
};

const PdfUploadButn = ({ handleUploadClick, pdf }) => {
    return <div className='flex gap-x-5 md:gap-x-10'>
        {pdf && <div className='flex gap-x-3 items-center'>

            <img src={pdfIcon} alt="pdf icon" />
            {/* restrict to show only 15 char of name */}
            <p className='block sm:hidden text-sm font-medium text-[rgba(15,169,88,1)]'>{pdf.filename.length > 15 ? pdf.filename.slice(0, 15) + '...' : pdf.filename}</p>
            <p className='hidden sm:block text-sm font-medium text-[rgba(15,169,88,1)]'>{pdf.filename}</p>
        </div>}
        <button
            className='flex gap-x-3 items-center py-2 px-2 md:px-6 rounded-xl border-2 border-black text-md'
            onClick={handleUploadClick}
        >
            <IoIosAddCircleOutline size={22} />
            <p className='hidden md:block font-bold'>Upload PDF</p>
        </button>
    </div>
}

export default Navbar;
