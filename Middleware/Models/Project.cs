using Middleware.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Datalayer.Models
{
    public class Project
    {
        public Guid Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }

        internal Guid CategoryId { get; set; }
        internal Category Category { get; set; }

        internal int UserId { get; set; }
        internal User User { get; set; }
    }
}
