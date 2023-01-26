using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Datalayer.Models
{
    public class UserClaim
    {
        public string Type { get; set; }
        [Key]
        public string Value { get; set; }
    }
}
