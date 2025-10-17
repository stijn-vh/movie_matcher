import PropTypes from "prop-types";
import React, { useState, useEffect, useRef } from 'react';
import { getAuth, onAuthStateChanged } from "firebase/auth";

interface Props {
    uid: string;
    onGroupJoined: (group: Group) => void;
} 

interface Group {
    id: string;
    name: string;
}

export const GroupList = ({ uid, onGroupJoined }: Props): JSX.Element => {
    const [groups, setGroups] = useState<Group[]>([])

    useEffect(() => {
        fetchGroups();
    }, []);

    useEffect(() => {}, []);

    const fetchGroups = async () => {
        fetch(`http://localhost:5000/group/all`)
            .then((response) => response.json())
            .then((data) => {
                data = data.groups
                setGroups(data)
            });
    };
    const handleJoinGroup = async (group: Group) => {
        const response = await fetch('http://localhost:5000/group/' + group.id + '/join', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ uid: uid }),
        });

        if (response.ok) {
            onGroupJoined(group)
        }
    }

    return (
        <ul className="list bg-primary-content rounded-box shadow-md w-1/2">
            <li className="p-4 pb-2 text-xs opacity-60 tracking-wide">Open groups:</li>
            {groups.map((group, index) => {
                return (              
                    <li className="flex items-center justify-between p-4 hover:bg-base-200">
                    <div className="flex items-center gap-3">
                        <div className="text-4xl font-thin opacity-30 tabular-nums">{index}</div>
                            <div>
                        <div>{group.name}</div>
                        <div className="text-xs uppercase font-semibold opacity-60">X people</div>
                        </div>
                    </div>
                    <div className="flex gap-2">
                        <button className="btn btn-square btn-ghost" onClick={() => handleJoinGroup(group)}>
                            <svg className="size-[1.2em]" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g stroke-linejoin="round" stroke-linecap="round" stroke-width="2" fill="none" stroke="currentColor"><path d="M6 3L20 12 6 21 6 3z"></path></g></svg>
                        </button>
                    </div>
            </li>
            )
        })}
        </ul>
)}

export default GroupList