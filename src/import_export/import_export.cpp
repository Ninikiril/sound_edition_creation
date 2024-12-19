#include "import_export/import_export.h"

namespace import_export{

const uint32_t RIFF = 0x46'46'49'52;
const uint32_t WAVE = 0x57'41'56'45;
const uint32_t FMT = 0x66'6D'74'20;
const uint32_t DATA = 0x64'61'74'61;
const uint32_t BYTE_SHIFT = 8;

bool CWavFile::fReadWav(const std::string &filename)
{
    bool success = true;
    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open())
    {
        success = false;
    }
    else
    {
        success = readHeader(file) && success;
        success = validateHeader() && success;
    }

    if (success)
    {
        success = readData(file) && success;
    }

    return success;
}

SWavHeader CWavFile::fGetHeader() const
{
    return pHeader;
}

std::vector<int16_t> CWavFile::fGetData() const
{
    return pData;
}

bool CWavFile::readHeader(std::ifstream &file)
{
    bool success = true;
    success = readType<uint32_t>(file, pHeader.chunkId) && success;
    success = readType<uint32_t>(file, pHeader.chunkSize) && success;
    success = readType<uint32_t>(file, pHeader.format) && success;
    success = readType<uint32_t>(file, pHeader.subchunk1Id) && success;
    success = readType<uint32_t>(file, pHeader.subchunk1Size) && success;
    success = readType<uint16_t>(file, pHeader.audioFormat) && success;
    success = readType<uint16_t>(file, pHeader.numChannels) && success;
    success = readType<uint32_t>(file, pHeader.sampleRate) && success;
    success = readType<uint32_t>(file, pHeader.byteRate) && success;
    success = readType<uint16_t>(file, pHeader.blockAlign) && success;
    success = readType<uint16_t>(file, pHeader.bitsPerSample) && success;
    success = readType<uint32_t>(file, pHeader.subchunk2Id) && success;
    success = readType<uint32_t>(file, pHeader.subchunk2Size) && success;
    return success;
}

bool CWavFile::validateHeader() const
{
    bool success = true;
    success = (pHeader.chunkId == RIFF) && success;
    success = (pHeader.format == WAVE) && success;
    success = (pHeader.subchunk1Id == FMT) && success;
    success = (pHeader.subchunk2Id == DATA) && success;
    return success;
}

bool CWavFile::readData(std::ifstream &file)
{
    bool success = true;
    const size_t size = pHeader.subchunk2Size / sizeof(int16_t);
    pData.resize(size);
    for (size_t i = 0; i < size; ++i)
    {
        success = readType<int16_t>(file, pData[i]) && success;
    }
    return success;
}

} // namespace import_export
