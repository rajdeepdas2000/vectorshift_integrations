import { useState, useEffect } from 'react';
import { Box, Button, CircularProgress } from '@mui/material';
import axios from 'axios';

export const HubspotIntegration = ({ user, org, integrationParams, setIntegrationParams }) => {
    const [isConnected, setIsConnected] = useState(false);
    const [isConnecting, setIsConnecting] = useState(false);

    const handleConnectClick = async () => {
        try {
            setIsConnecting(true);
            const formData = new FormData();
            formData.append('user_id', user);
            formData.append('org_id', org);

            const response = await axios.post(
                'http://localhost:8000/integrations/hubspot/authorize',
                formData
            );

            const authURL = response.data;

            const newWindow = window.open(authURL, 'HubSpot Auth', 'width=600,height=600');

            const timer = setInterval(() => {
                if (newWindow.closed) {
                    clearInterval(timer);
                    handleWindowClosed();
                }
            }, 500);
        } catch (e) {
            setIsConnecting(false);
        }
    };

    const handleWindowClosed = async () => {
        const formData = new FormData();
        formData.append('user_id', user);
        formData.append('org_id', org);

        const response = await axios.post(
            'http://localhost:8000/integrations/hubspot/credentials',
            formData
        );

        const credentials = response.data;

        setIntegrationParams({
            credentials,
            type: 'HubSpot'
        });

        setIsConnected(true);
        setIsConnecting(false);
    };

    useEffect(() => {
        setIsConnected(!!integrationParams?.credentials);
    }, []);

    return (
        <Box sx={{ mt: 2 }}>
            <Button
                variant="contained"
                onClick={handleConnectClick}
                disabled={isConnecting || isConnected}
            >
                {isConnected ? "HubSpot Connected" : isConnecting ? <CircularProgress size={20} /> : "Connect HubSpot"}
            </Button>
        </Box>
    );
};