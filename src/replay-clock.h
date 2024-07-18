#ifndef REPCL_H
#define REPCL_H

#include "replay-config.h"

#include <bitset>
#include <sstream>
#include <string>
#include <cstdint>

class ReplayClock
{

public:

    /**
     *  Assignment operator
     * \param [in] o ReplayClock to assign.
     * \return The ReplayClock.
     */
    inline ReplayClock &operator=(const ReplayClock &o)
    {
        if (this != &o)
        {
            nodeId          = o.nodeId;
            hlc             = o.hlc;
            offset_bitmap   = o.offset_bitmap;
            counters        = o.counters;
            offsets         = o.offsets;
            epsilon         = o.epsilon;
            interval        = o.interval;
        }
        return *this;
    }


    /** Default constructor, with value 0. */
    inline ReplayClock() : hlc(), offset_bitmap(), offsets(), counters(), nodeId(), epsilon(), interval()
    {
        // Set offset of node to 0
        offset_bitmap[nodeId] = 0;
    } 


    /** Specification constructor. */
    inline ReplayClock(uint32_t hlc, uint32_t nodeId, uint32_t epsilon, uint32_t interval) : hlc(hlc), nodeId(nodeId), epsilon(epsilon), interval(interval) 
    {
        offset_bitmap   = 0;
        offsets         = 0;
        counters        = 0;

        // Set offset of node to 0
        offset_bitmap[nodeId] = 0;
    }

    /** Specification constructor. */
    inline ReplayClock(uint32_t hlc, uint32_t nodeId, std::bitset<NUM_PROCS> offset_bitmap, std::bitset<64> offsets, uint32_t counters, uint32_t epsilon, uint32_t interval) : hlc(hlc), offset_bitmap(offset_bitmap), offsets(offsets), counters(counters), nodeId(nodeId), epsilon(epsilon), interval(interval) 
    {}    


    /** Constructor from string representation */
    inline ReplayClock(std::string replayClockString, uint32_t nodeId, uint32_t epsilon, uint32_t interval) : nodeId(nodeId), epsilon(epsilon), interval(interval)
    {

        std::istringstream ss(replayClockString);
        ss >> hlc >> offset_bitmap >> offsets >> counters;

    }


    /**
     *  Copy constructor
     *
     * \param [in] o ReplayClock to copy
     */
    inline ReplayClock(const ReplayClock &o)
    {
        nodeId          = o.nodeId;
        hlc             = o.hlc;
        offset_bitmap   = o.offset_bitmap;
        counters        = o.counters;
        offsets         = o.offsets;
        epsilon         = o.epsilon;
        interval        = o.interval;
    }


    /**
     * EqualOffset operation to check whether the two clocks are equal.
     * \param [in] o ReplayClock to check current clock with
    */
    bool IsEqual(ReplayClock o);


    /** Destructor */
    ~ReplayClock() {}    

    
    inline uint32_t GetNodeId() const
    {
        return nodeId;
    }


    inline uint32_t GetHLC() const
    {
        return hlc;
    }


    inline std::bitset<NUM_PROCS> GetBitmap() const 
    {
        return offset_bitmap;
    }


    inline std::bitset<64> GetOffsets() const
    {
        return offsets;
    }


    /**
     * GetOffsetAtIndex operation to get only the offset of one index..
     * \param [in] index The index of the offset to get
    */
    uint32_t GetOffsetAtIndex(uint32_t index);


    inline uint32_t GetCounters() const
    {
        return counters;
    }


    uint32_t GetOffsetSize();


    uint32_t GetCounterSize();


    uint32_t GetClockSize();

    uint32_t GetMaxOffset();


    void SetNodeId(uint32_t nodeId_) 
    {
        nodeId = nodeId_;
    }


    void SetHLC(uint32_t hlc_)
    {
        hlc = hlc_;
    }


    void SetOffsets(std::bitset<64> offsets_) 
    {
        offsets = offsets_;
    }


    /**
     * SetOffsetAtIndex operation to set only the offset of one index.
     * \param [in] index The index of the offset to set
     * \param [in] newOffset The new offset to set the index to
    */
    void SetOffsetAtIndex(uint32_t index, uint32_t newOffset);


    void SetCounters(uint32_t counters_)
    {
        counters = counters_;
    }


    void SetOffsetBitmap(std::bitset<NUM_PROCS> offset_bitmap_)
    {
        offset_bitmap = offset_bitmap_;
    }


    /**@}*/ // Create ReplayClock from Values and Units

    /**
     * \name Get ReplayClock as Strings
     * Get the ReplayClock as Strings.
     *
     * @{
     */
    /**
     * Get the ReplayClock value expressed in a string.
     *
     * \return The ReplayClock expressed in a string
     */
    inline std::string ToString() const
    {
        std::ostringstream ss;

        ss << hlc << " " << offset_bitmap << " " << offsets << " " << counters;

        return ss.str();
    }


    /**
     * Send/Local operation to advance the ReplayClock.
     * \param [in] node_hlc The local node clock
    */
    void SendLocal(uint32_t node_hlc);


    /**
     * Recv operation to process incoming clocks to the ReplayClock.
     * \param [in] m_ReplayClock The event node clock
     * \param [in] node_hlc The local node clock
    */
    void Recv(ReplayClock m_ReplayClock, uint32_t node_hlc);


    /**
     * Shift operation to shift the ReplayClock by the local node clock update.
     * \param [in] node_hlc The local node clock
    */
    void Shift(uint32_t node_hlc);


    /**
     * MergeSameEpoch operation to shift the ReplayClock by the incoming message's node clock offset.
     * \param [in] m_ReplayClock The event node clock
    */
    void MergeSameEpoch(ReplayClock m_ReplayClock);


    /**
     * EqualOffset operation to check whether the offsets of two clocks are equal.
     * \param [in] o ReplayClock to check current clock with
    */
    bool EqualOffset(ReplayClock o) const;


    /**
     * RemoveOffsetAtIndex operation to remove an offset at an index.
     * \param [in] index Offset to remove by index
    */
    void RemoveOffsetAtIndex(uint32_t index);

    /**
     * PrintClock operation to print the clock.
    */
    void PrintClock();



private:
    uint32_t                                    hlc;               //!< Hybrid Logical Clock for topmost level
    std::bitset<NUM_PROCS>                      offset_bitmap;     //!< Offset bitmap that stores true for nodes whose offsets are being tracked
    std::bitset<64>                             offsets;           //!< Value of offsets for the nodes where bitmap denotes true
    uint32_t                                    counters;          //!< Counters for events occuring within an interval
    uint32_t                                    nodeId;            //!< NodeID of the current node
    uint32_t                                    epsilon;           //!< Maximum acceptable clock skew
    uint32_t                                    interval;          //!< Discretizing the standard flow of time to save space

};

#endif /* REPCL_H */
