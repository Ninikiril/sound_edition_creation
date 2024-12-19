#pragma once

#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace import_export {
/// @brief struct for .wav header
/// @details This struct contains the header of a .wav file

struct SWavHeader
{
    uint32_t chunkId;
    uint32_t chunkSize;
    uint32_t format;
    uint32_t subchunk1Id;
    uint32_t subchunk1Size;
    uint16_t audioFormat;
    uint16_t numChannels;
    uint32_t sampleRate;
    uint32_t byteRate;
    uint16_t blockAlign;
    uint16_t bitsPerSample;
    uint32_t subchunk2Id;
    uint32_t subchunk2Size;
};

/// @brief class to read a .wav file
/// @details This class contains a header and data of a .wav file
/// and a method to read the data from the file

class CWavFile
{
public:
    /// @brief constructor
    CWavFile() = default;

    /// @brief destructor
    ~CWavFile() = default;

    /// @brief Method to read the data from a .wav file
    /// @param filename The name of the file to read
    /// @return True if the file was read successfully, false otherwise
    bool fReadWav(const std::string &filename);

    /// @brief Method to get the header from the .wav file
    /// @return The header from the .wav file
    SWavHeader fGetHeader() const;

    /// @brief Method to get the data from the .wav file
    /// @return The data from the .wav file
    std::vector<int16_t> fGetData() const;

private:
    /// @brief Method to read the header from a .wav file
    /// @param file The file to read from
    /// @return True if the header was read successfully, false otherwise
    bool readHeader(std::ifstream &file);

    /// @brief Method to validate the header from a .wav file
    /// @return True if the header is valid, false otherwise
    bool validateHeader() const;

    /// @brief Method to read the data from a .wav file
    /// @param file The file to read from
    /// @return True if the data was read successfully, false otherwise
    bool readData(std::ifstream &file);

    /// @brief Method to read a type_t from a file
    /// @param file The file to read from
    /// @param value The value to read
    /// @return True if the value was read successfully, false otherwise
    template <typename type_t>
    bool readType(std::ifstream &file, type_t &value)
    {
        bool success = true;
        const size_t size = sizeof(type_t) / sizeof(char);
        std::array<char, size> buffer;
        if (!file.read(buffer.data(), buffer.size()))
        {
            success = false;
        }
        else
        {
            value = 0;
            for(size_t i = 0; i < size; ++i)
            {
                value |= static_cast<type_t>(buffer[i])
                << static_cast<type_t>(i * BYTE_SHIFT);
            }
        }
        return success;
    }

    /// @brief The header of the .wav file
    SWavHeader pHeader;

    /// @brief The data of the .wav file
    std::vector<int16_t> pData;
};

} // namespace import_export
