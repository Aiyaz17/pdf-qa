import React, { useState, useRef, useEffect } from 'react';
import { LuSendHorizonal } from "react-icons/lu";
import UserProfile from "../assets/user-profile.png";
import botProfile from "../assets/bot-profile.png";
import axios from 'axios';
import { toast } from 'react-toastify';
import { Comment } from 'react-loader-spinner';

const Chat = ({ pdf }) => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [sessionId, setSessionId] = useState(null);
    const chatEndRef = useRef(null);

    useEffect(() => {
        if (chatEndRef.current) {
            chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    useEffect(() => {
        if (pdf) {
            setMessages([{ content: 'Hi there! Ask me anything about the uploaded PDF!', sender: 'bot' }]);
        } else {
            setMessages([]);
        }
    }, [pdf]);

    const handleSend = async (e) => {
        e.preventDefault();

        if (!input) {
            toast.error('Please enter a message', {
                position: "top-center",
                autoClose: 3000,
            });
            return;
        }

        const newMessages = [...messages, { content: input, sender: 'user' }, {
            content:
                <Comment
                    visible={true}
                    height="35"
                    width="40"
                    ariaLabel="comment-loading"
                    wrapperStyle={{}}
                    wrapperClass="comment-wrapper"
                    color="#fff"
                    backgroundColor="gray"
                />
            , sender: 'bot'
        }];

        setMessages(newMessages);
        setInput('');
        chatEndRef.current.scrollIntoView({ behavior: 'smooth' });

        try {
            var path = sessionId == null ? '/start_conversation/' : '/follow_up/';
            var body = sessionId == null ? { "query": input, "pdf_document_id": pdf.id } : { "session_id": sessionId, "query": input };
            const response = await axios.post(path, body);

            if (response.status === 200) {
                newMessages.pop();
                setMessages([...newMessages, { content: response.data.response, sender: 'bot' }]);
                if (sessionId == null)
                    setSessionId(response.data.session_id);
            } else {
                throw new Error('Error sending message');
            }

        } catch (error) {
            console.log(error);
            toast.error('Error sending message, Please Try again in some time', {
                position: "top-center",
                autoClose: 3000,
            });
            newMessages.pop();
        }
    };

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    return (
        <div className='w-[95%] mx-auto sm:mx-10 sm:w-auto  lg:mx-28 my-16 '>
            <div className="flex flex-col ">
                <div className="flex-1 p-4">
                    {
                        messages.map((message, index) => (
                            <Message key={index} message={message} />
                        ))
                    }
                    <div ref={chatEndRef} />
                </div>
                <div className="flex p-4  fixed bottom-5 left-0 right-0 z-[10] ">
                    <form className="relative bg-white flex-1 max-w-[1300px] mx-auto shadow-[0px_4px_30px_0px_rgba(102,102,102,0.1)]" onSubmit={handleSend}>
                        <input
                            type="text"
                            value={input}
                            onChange={handleInputChange}
                            className="w-full px-5 py-3 border border-gray-300 rounded-md focus:outline-none text-sm disabled:bg-gray-100"
                            placeholder="Send a message..."
                            disabled={!pdf}
                        />
                        <button
                            onClick={handleSend}
                            disabled={!pdf}
                            className="absolute right-2 top-1/2 transform -translate-y-1/2 text-neutral-500 p-2 focus:outline-none"
                        >
                            <LuSendHorizonal size={24} />
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

const Message = ({ message }) => {
    // check if content is a string or a component
    const { content, sender } = message;

    var isString = content && typeof content === 'string';
    var lenOfSentence = isString ? content.split(" ").length : 0;

    return (
        <div className={`my-8 flex gap-x-5 ${lenOfSentence < 30 ? 'items-center' : 'items-start'} `}>
            <div className='w-[40px]'>
                <img
                    src={sender === 'bot' ? botProfile : UserProfile}
                    alt="Profile"
                    className={`w-full h-full min-w-[40px] rounded-full}`}
                />
            </div>
            <div
                className={`inline-block rounded-lg leading-7 ${!isString && "transform scale-x-[-1]"}`}
            >
                {content}
            </div>
        </div>
    );
}

export default Chat;
