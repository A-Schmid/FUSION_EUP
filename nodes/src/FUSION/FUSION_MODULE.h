#ifndef FUSION_MODULE_H
#define FUSION_MODULE_H

#define INDEX_FRAME_BEGIN 0
#define INDEX_FRAME_ID 1
#define INDEX_MSG_ID 2
#define INDEX_NI 3
#define INDEX_NMB_DATA 4

#define FRAME_HEAD_LENGTH 4
#define FRAME_CHECKSUM_LENGTH 2
#define FRAME_BEGIN 0xAA

class FusionModule
{
    public:
        FusionModule(unsigned int ni);
        unsigned int nodeId;
        unsigned int packetLength;
        char* packet;

        void createPacket(char* data, int data_length);
        void freePacket();
};

#endif // FUSION_MODULE_H
